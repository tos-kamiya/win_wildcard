# ref: https://stackoverflow.com/questions/55597797/detect-whether-current-shell-is-powershell-in-python

from typing import List, Optional
import locale
import os
import psutil
import re
import subprocess


SUBPROCESS_OUT_ENCODING = locale.getpreferredencoding()


def get_windows_shell() -> Optional[str]:
    '''
    Determine if the shell that executed the script is PowerShell or cmd.exe.
    The return value is 'powershell' if the shell from which the script was executed is PowerShell, 'cmd' if it is cmd.exe, or None otherwise.
    '''

    pprocName = psutil.Process(os.getppid()).name()

    if re.fullmatch('pwsh|pwsh.exe|powershell.exe', pprocName):
        return 'powershell'

    if re.fullmatch('cmd.exe', pprocName):
        return 'cmd'

    return None


def expand_windows_wildcard(filename: str, only_files=False) -> List[str]:
    '''
    Expand a wildcard if the script is running in a Windows shell and if the filename of the argument contains the wildcard.
    The return value is a list of expanded file names and/or directory names. In case of no expansion, the list contains only the given filename.
    '''

    if not (filename.find('*') >= 0 or filename.find('?') >= 0):
        return [filename]

    s = get_windows_shell()
    if s == 'powershell':
        cmd = ['powershell.exe', '-Command', 'Get-ChildItem']
        if only_files:
            cmd.append('-File')
        cmd.extend(['-Name', filename])
        out = subprocess.check_output(cmd)
    elif s == 'cmd':
        cmd = ['dir']
        if only_files:
            cmd.append('/A-D')
        cmd.extend(['/B', filename])
        out = subprocess.check_output(cmd, shell=True)
    else:
        return [filename]

    text = out.decode(SUBPROCESS_OUT_ENCODING)
    r = []
    for L in text.split('\n'):
        if L:
            r.append(L)
    return r


if __name__ == '__main__':
    import sys

    if get_windows_shell() is None:
        sys.exit('script executed outside of Windows cmd.exe or powershell')

    files = []
    for a in sys.argv[1:]:
        r = expand_windows_wildcard(a)
        files.extend(r)

    print('\n'.join(files))
