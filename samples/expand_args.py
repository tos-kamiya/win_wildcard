import sys

from win_wildcard import expand_windows_wildcard

files = []
for a in sys.argv[1:]:
    r = expand_windows_wildcard(a)
    files.extend(r)

print('\n'.join(files))
