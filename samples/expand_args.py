import sys

from win_wildcard import expand_windows_wildcard

files = []
for a in sys.argv[1:]:
    r = expand_windows_wildcard(a)
    if not r:
        print("warning: no matching files for the wildcard: %s" % a)
        continue
    files.extend(r)

if files:
    print('\n'.join(files))
