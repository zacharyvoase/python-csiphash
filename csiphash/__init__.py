"""
The SipHash-2-4 C reference implementation, wrapped with CFFI.

Currently doesn't support the full hashlib interface, just a function that
accepts and returns byte strings.

Basic usage::

    >>> siphash24(b'\\x00' * 16, b'hello, world!\\n')
    b'\\xf1G4\\x95\\xa5\\xaa\\xc2b'

If you want to specify keys in hexadecimal, use ``.decode('hex')``::

    >>> siphash24('abcdef01234567899876543210fedcba'.decode('hex'), b'hello, world!\\n')
    '\\xd3\\xd4N\\x1dk\\x1f$='

If you want digests in hexadecimal, use ``.encode('hex')``::

    >>> siphash24(b'\\x00' * 16, b'hello, world!\\n').encode('hex')
    'f1473495a5aac262'
"""

from . import six
from ._siphash import ffi, lib


def siphash24(key, data):
    """
    Apply SipHash-2-4 to a bytestring.

    :param key: a byte string of length 16 to use as the secret key
    :param data: a byte string of arbitrary length to hash
    :returns: the hash output, as a byte string of length 8
    """
    if not isinstance(key, six.binary_type):
        raise TypeError("key must be a bytestring")
    if len(key) != 16:
        raise ValueError("key must be 16 bytes long")
    if not isinstance(data, six.binary_type):
        raise TypeError("data must be a bytestring")

    out_arr = ffi.new('uint8_t[8]')
    in_arr = ffi.cast('uint8_t *', ffi.from_buffer(data))
    key_arr = ffi.cast('uint8_t *', ffi.from_buffer(key))

    result = lib.siphash(out_arr, in_arr, len(data), key_arr)
    if result == 0:
        return ''.join(map(six.int2byte, ffi.unpack(out_arr, 8)))
    raise RuntimeException("SipHash failed with error code {}".format(result))
