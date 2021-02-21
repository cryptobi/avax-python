#!/usr/bin/envpython

"""Testsfor`cb58ref`package."""

import codecs

import pytest

import cb58ref

# From https://www.di-mgt.com.au/sha_testvectors.html
SHA256_TEST_VECTORS = [
    (
        b'abc',
        'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
    ),
    (
        b'',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    ),
    (
        b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
        '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1',
    ),
    (
        b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu',  # noqa: E501
        'cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1',
    ),
    (
        b'a'*1000000,
        'cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0'
    ),
]


# From https://github.com/ava-labs/gecko/blob/b1923d7dee51dba7b8ddc6e64b396f44b25c44cc/utils/formatting/cb58_test.go  # noqa: E501
CB58_TEST_VECTORS = [
    (
        bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 255]),
        '1NVSVezva3bAtJesnUj',
    ),
    (
        bytearray([0]),
        '1c7hwa',
    ),
]


@pytest.mark.parametrize('v,hexdigest', SHA256_TEST_VECTORS)
def test_cb58checksum(v, hexdigest):
    digest = codecs.decode(hexdigest, 'hex')
    assert cb58ref.cb58checksum(v) == digest[28:32]


@pytest.mark.parametrize('expected,encoded', CB58_TEST_VECTORS)
def test_cb58decode(encoded, expected):
    assert cb58ref.cb58decode(encoded) == expected


@pytest.mark.parametrize('unencoded,expected', CB58_TEST_VECTORS)
def test_cb58encode(unencoded, expected):
    assert cb58ref.cb58encode(unencoded) == expected
