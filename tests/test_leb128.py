
from byteme import leb128_encode, leb128_decode


def test_leb128_known_values():

    test_vectors = [
        ('00', 0x00, 0x00),
        ('01', 0x01, 0x01),

        # From https://github.com/Medium/leb
        ('10', 0x10, 0x10),
        ('45', 0x45, -0x3b),
        ('8e 32', 0x190e, 0x190e),
        ('c1 57', 0x2bc1, -0x143f),
        ('80 80 80 3f', 0x7e00000, 0x7e00000),
        ('80 80 80 4f', 0x9e00000, -0x6200000),

        # From http://en.wikipedia.org/wiki/LEB128
        ('e5 8e 26', 624485, None),
        ('9b f1 59', None, -624485),


        # From http://events.linuxfoundation.org/sites/events/
        #      files/slides/ABS2014.pdf
        ('7f', 127, -1),
        ('807f', 16256, -128),
    ]

    for s, positive, negative in test_vectors:
        b = bytes.fromhex(s)

        if positive is not None:
            assert leb128_encode(positive) == b
            decoded, size = leb128_decode(b)
            assert decoded == positive
            assert len(b) == size

        if negative is not None:
            assert leb128_encode(negative, signed=True) == b
            decoded, size = leb128_decode(b, signed=True)
            assert decoded == negative
            assert len(b) == size


def test_leb128_roundtrip():
    for i in range(-123456789, 123456789, 100000):
        if i >= 0:
            encoded = leb128_encode(i)
            decoded, _ = leb128_decode(encoded)
            assert decoded == i

        encoded = leb128_encode(i, signed=True)
        decoded, _ = leb128_decode(encoded, signed=True)
        assert decoded == i


def test_leb128_trailing_bytes():
    # It should ignore trailing bytes after the terminating byte
    assert leb128_decode(b'\xe5\x8e\x26\xab\xab\xab') == (624485, 3)
