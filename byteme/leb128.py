"""
Module for encoding and decoding LEB128 values.

http://en.wikipedia.org/wiki/LEB128
"""


def leb128_encode(value, signed=False):
    if not signed and value < 0:
        raise ValueError("Value cannot be negative.")

    buf = bytearray()
    more = True

    while more:

        # Obtain the lowest 7 bits, and shift the remainder.
        byte = value & 0x7f
        value >>= 7

        # For signed numbers, use sign extension to ensure that the
        # MSB is 0 for positive numbers, and 1 for negative numbers.
        if signed:
            if value == 0 and byte & 0x40 == 0:
                # Last byte for positive number
                more = False
            elif value == -1 and byte & 0x40:
                # Last byte for negative number
                more = False
            else:
                # Not done yet
                byte |= 0x80

        # Unsigned numbers do not have a sign bit.
        else:
            if value:
                # Not done yet
                byte |= 0x80
            else:
                more = False

        buf.append(byte)

    return bytes(buf)


def leb128_decode(value, signed=False):
    decoded = 0
    shift = 0

    for size, byte in enumerate(value, 1):
        decoded |= (byte & 0x7f) << shift
        shift += 7
        if byte & 0x80 == 0:
            break

    # Negative numbers have a sign bit in the last byte.
    if signed and byte & 0x40:
        decoded -= (1 << shift)

    return decoded, size
