"""
Python 2/3 compatibility code.

Taken from, or inspired by, the 'six' library.
"""

import sys


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    iterbytes = iter
    map = map

else:
    import functools
    import itertools

    iterbytes = functools.partial(itertools.imap, ord)
    map = itertools.imap
