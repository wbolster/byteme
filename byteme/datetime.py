"""
Date/time encoding routines.
"""

import struct

# http://dev.mysql.com/doc/internals/en/
#    date-and-time-data-type-representation.html
#
#  1 bit  sign           (1= non-negative, 0= negative)
# 17 bits year*13+month  (year 0-9999, month 0-12)
#  5 bits day            (0-31)
#  5 bits hour           (0-23)
#  6 bits minute         (0-59)
#  6 bits second         (0-59)
# ---------------------------
# 40 bits = 5 bytes
#
# TODO: microseconds= arg, use 8 bytes instead of 5 in that case
# TODO: support for partial dates (e.g. month=0) gracefully, but
#       built-in datetime module doesn't support it :(


def mysql_datetime_dumps(dt):

    n = ((1 << 39)  # sign bit
         + ((dt.year * 13 + dt.month) << 22)
         + (dt.day << 17)
         + (dt.hour << 12)
         + (dt.minute << 6)
         + dt.second)
    return struct.pack('>Q', n)[-5:]


def mysql_datetime_dump(value, fp):
    fp.write(mysql_datetime_dumps(value))


def mysql_datetime_loads(value):
    raise NotImplementedError()


def mysql_datetime_load(value, fp):
    # TODO: handle partial reads
    return mysql_datetime_loads(fp.read(5))
