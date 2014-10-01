"""
Module for encoding and decoding LEB128 values.

http://en.wikipedia.org/wiki/LEB128
"""


def leb128_encode(value, signed=False):
    buf = bytearray()

    if signed:
        raise NotImplementedError()

    else:
        if value < 0:
            raise ValueError("Value cannot be negative.")

        while value > 0x7f:
            buf.append((value & 0x7f) | 0x80)
            value >>= 7
        buf.append(value)

    return bytes(buf)


def leb128_decode(value, signed=False):

    decoded = 0

    if signed:
        size = 0  # FIXME:
        raise NotImplementedError()
    else:
        shift = 0
        for size, byte in enumerate(value, 1):
            decoded |= (byte & 0x7f) << shift
            shift += 7
            if byte & 0x80 == 0:
                break

    return decoded, size


def test_leb128():

    test_vectors = [
        # From https://github.com/Medium/leb
        ('10', 0x10),
        ('45', 0x45),
        ('8e 32', 0x190e),
        ('c1 57', 0x2bc1),
        ('80 80 80 3f', 0x7e00000),
        ('80 80 80 4f', 0x9e00000),

        # From http://en.wikipedia.org/wiki/LEB128
        ('e5 8e 26', 624485),
    ]

    for s, n in test_vectors:
        b = bytes.fromhex(s)

        assert leb128_encode(n) == b
        decoded, size = leb128_decode(b)
        assert decoded == n

    # It should ignore trailing bytes after the terminating byte
    assert leb128_decode(b'\xe5\x8e\x26\xab\xab\xab') == (624485, 3)
