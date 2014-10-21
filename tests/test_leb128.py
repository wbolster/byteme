
import binascii
import io

import pytest

import byteme


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
        ('80 7f', 16256, -128),
    ]

    for s, positive, negative in test_vectors:
        b = binascii.unhexlify(s.replace(' ', ''))

        if positive is not None:
            assert byteme.leb128_dumps(positive) == b
            decoded, size = byteme.leb128_loads(b)
            assert decoded == positive
            assert len(b) == size

        if negative is not None:
            assert byteme.leb128_dumps(negative, signed=True) == b
            decoded, size = byteme.leb128_loads(b, signed=True)
            assert decoded == negative
            assert len(b) == size


def test_leb128_roundtrip():
    for i in range(-123456789, 123456789, 100000):
        if i >= 0:
            encoded = byteme.leb128_dumps(i)
            decoded, _ = byteme.leb128_loads(encoded)
            assert decoded == i

        encoded = byteme.leb128_dumps(i, signed=True)
        decoded, _ = byteme.leb128_loads(encoded, signed=True)
        assert decoded == i


def test_leb128_trailing_bytes():
    # It should ignore trailing bytes after the terminating byte
    assert byteme.leb128_loads(b'\xe5\x8e\x26\xab\xab\xab') == (624485, 3)


def test_leb128_limits():

    with pytest.raises(ValueError):
        byteme.leb128_loads(b'\x8e\x32', max=1)

    with pytest.raises(ValueError):
        byteme.leb128_loads(b'\x9b\xf1\x59', signed=True, max=2)


def test_leb128_truncated():
    with pytest.raises(ValueError):
        byteme.leb128_loads(b'\x80')


def test_leb128_file_like():
    fp = io.BytesIO(b'\x80\x7fabc')
    value = byteme.leb128_load(fp, signed=True)
    assert value == -128
    assert fp.read() == b'abc'

    res = byteme.leb128_load(
        io.BytesIO(b'\x80\x7f'),
        signed=True,
        only_value=False)
    assert res == (-128, 2)

    fp = io.BytesIO()
    byteme.leb128_dump(-128, fp, signed=True)
    assert fp.getvalue() == b'\x80\x7f'
