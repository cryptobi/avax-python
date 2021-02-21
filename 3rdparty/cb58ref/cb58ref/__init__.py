"""Top-level package for cb58ref."""

__author__ = 'Alex Willmer'
__email__ = 'alex@moreati.org.uk'
__version__ = '0.2.0'

from .base58 import SHA256, b58chars as cb58chars, b58decode, b58encode

__all__ = [
    'Error',
    'ChecksumError',
    'DecodeError',
    'EncodeError',
    'cb58chars',
    'cb58checksum',
    'cb58decode',
    'cb58encode',
]


class Error(ValueError):
    pass


class DecodeError(Error):
    pass


class ChecksumError(DecodeError):
    pass


class EncodeError(Error):
    pass


def cb58checksum(v: bytes) -> bytes:
    """Return a 32-bit checksum of v, derived from the end of a SHA256 digest.
    """
    h = SHA256.new(v)
    return h.digest()[-4:]


def cb58decode(v: str) -> bytes:
    """Return the bytes encoded within the CB58 value v.
    """
    result = b58decode(v)
    if result is None:
        raise DecodeError
    body = result[:-4]
    checksum = result[-4:]
    if checksum == cb58checksum(body):
        return body
    else:
        raise ChecksumError


def cb58encode(v: bytes) -> str:
    """Return a CB58 encoded representation of v.
    """
    return b58encode(v + cb58checksum(v))
