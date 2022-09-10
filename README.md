win_wildcard
============

Expand wildcards in shells of Windows using the dir or the Get-ChildItem command.

## Sample

```python
import sys
from win_wildcard import expand_windows_wildcard

files = []
for a in sys.argv[1:]:
    r = expand_windows_wildcard(a)
    files.extend(r)

print('\n'.join(files))
```

## Motivation

Python has a `glob` module that supports posix-spec wildcards, so it is possible to create scripts with wildcards available. However, for the reasons described below, glob's wildcard is not the same as expected on the Windows command line.

The Windows shell leaves wildcard expansion to the command, so there is no standard way to expand wildcards.

* [Wildcards of Get-ChildItem command of PowerShell](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_wildcards?view=powershell-7.2)
* [Wildcards of dir command of cmd.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/dir)

Some wildcards of cmd.exe are undocumented.

* [Wildcards of Win32API FindFirstFile](https://stackoverflow.com/questions/2563316/findfirstfileex-wildcard-characters)
* [Undocumented Wildcards](https://vs-rennweg.ksn.at/allmann/allgemeines/1/scripts%20kommandozeile/Windows%20CMD%20Shell%20Command%20Line%20Syntax/Wildcards%20_%20Windows%20CMD%20_%20SS64.com.html)

There have been reports of user confusion due to wildcard specifications varying from command to command.

* [PowerShell allow to use wildcard while copying file but cmd don't allow , why?](https://stackoverflow.com/questions/30427288/powershell-allow-to-use-wildcard-while-copying-file-but-cmd-dont-allow-why)
* [Globbing patterns in windows command prompt/ powershell](https://stackoverflow.com/questions/72434739/globbing-patterns-in-windows-command-prompt-powershell)

I thought it would be appropriate to provide a function that calls the `dir` command or `Get-ChildItem` command and uses the result of expanding the wildcard.

Such wildcard expansion would allow the user to run the dir or Get-ChildItem command to see what files are specified before executing the script.
