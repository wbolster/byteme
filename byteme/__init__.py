"""
byteme, a collection of serialisation and encoding routines
"""

# This module only expose public API

from .leb128 import (  # noqa
    leb128_dump,
    leb128_dumps,
    leb128_load,
    leb128_loads,
)
