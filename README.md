win_wildcard
============

Expanding wildcards in shells of Windows using the dir or the ls commands.

## Sample

```python
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
* [Wildcards of FindFirstFile(stackoverflow)](https://stackoverflow.com/questions/2563316/findfirstfileex-wildcard-characters)

I thought it would be appropriate to provide a function that calls the `dir` command or `Get-ChildItem` command and uses the result of expanding the wildcard.

Such wildcard expansion would allow the user to run the dir or Get-ChildItem command to see what files are specified before executing the script.
