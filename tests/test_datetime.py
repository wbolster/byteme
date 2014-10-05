
import datetime

import byteme


def test_datetime():
    dt = datetime.datetime(2014, 10, 5, 1, 2, 3)

    # Sign, year (includes month), day, hour, minute, second:
    #          SYYYYYYY    YYYYYYYY    YYDDDDDH    HHHHMMMM    MMSSSSSS
    parts = [0b10011001, 0b10010100, 0b00001010, 0b00010000, 0b10000011]
    as_bytes = bytes(bytearray(parts))

    assert byteme.mysql_datetime_dumps(dt) == as_bytes
    assert byteme.mysql_datetime_loads(as_bytes) == dt
