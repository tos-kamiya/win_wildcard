from typing import List, Optional
import locale
import os
import psutil
import re
import subprocess


SUBPROCESS_OUT_ENCODING = locale.getpreferredencoding()

POWERSHELL_META_CHARACTERS = "*?[]`"
CMD_META_CHARACTERS = "*?<>" + '"'


def get_windows_shell() -> Optional[str]:
    '''
    Determine if the shell that executed the script is PowerShell or cmd.exe.
    The return value is 'powershell' if the shell from which the script was executed is PowerShell, 'cmd' if it is cmd.exe, or None otherwise.
    '''

    # ref: https://stackoverflow.com/questions/55597797/detect-whether-current-shell-is-powershell-in-python

    pprocName = psutil.Process(os.getppid()).name()

    if re.fullmatch('pwsh|pwsh.exe|powershell.exe', pprocName):
        return 'powershell'

    if re.fullmatch('cmd.exe', pprocName):
        return 'cmd'

    return None


def expand_powershell_wildcard(filename: str, only_files: bool = False) -> List[str]:
    '''
    Expand wildcards of PowerShell.
    The return value is a list of expanded file names and/or directory names.
    Returns a list contains only the given filename when no wildcard chars included in the filename.
    Returns an empty list when there are no files matching the wildcard.
    '''

    if not any(filename.find(mc) >= 0 for mc in POWERSHELL_META_CHARACTERS):
        return [filename]

    cmd = ['powershell.exe', '-Command', 'Get-ChildItem']
    if only_files:
        cmd.append('-File')
    cmd.extend(['-Name', filename])
    out = subprocess.check_output(cmd)

    text = out.decode(SUBPROCESS_OUT_ENCODING)
    r = []
    for L in text.split('\n'):
        if L:
            r.append(L)
    return r


def expand_cmd_wildcard(filename: str, only_files: bool = False) -> List[str]:
    '''
    Expand wildcards of cmd.exe.
    The return value is a list of expanded file names and/or directory names.
    Returns a list contains only the given filename when no wildcard chars included in the filename.
    Returns an empty list when there are no files matching the wildcard.
    '''

    if not any(filename.find(mc) >= 0 for mc in CMD_META_CHARACTERS):
        return [filename]

    cmd = ['dir']
    if only_files:
        cmd.append('/A-D')
    cmd.extend(['/B', filename])
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)  # do not show error message when there are no matching files
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:  # there are no matching files
            return []
        raise e

    text = out.decode(SUBPROCESS_OUT_ENCODING)
    r = []
    for L in text.split('\n'):
        if L:
            r.append(L)
    return r


SHELL_TO_EXPAND_WILDCARD_FUNC = {'powershell': expand_powershell_wildcard, 'cmd': expand_cmd_wildcard}


def expand_windows_wildcard(filename: str, only_files: bool = False) -> List[str]:
    '''
    Expand wildcards when the script is running in a Windows shell and when the filename contains wildcards.
    The return value is a list of expanded file names and/or directory names.
    Returns a list contains only the given filename when no wildcard chars included in the filename.
    Returns an empty list when there are no files matching the wildcard.
    '''

    s = get_windows_shell()
    if s is None:
        return [filename]

    f = SHELL_TO_EXPAND_WILDCARD_FUNC.get(s, None)
    if f is not None:
        return f(filename, only_files=only_files)
    else:
        return [filename]


if __name__ == '__main__':
    import sys

    if get_windows_shell() is None:
        sys.exit('script executed outside of Windows cmd.exe or powershell')

    files = []
    for a in sys.argv[1:]:
        r = expand_windows_wildcard(a)
        files.extend(r)

    print('\n'.join(files))
