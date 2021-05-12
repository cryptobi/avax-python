# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Find tutorials and use cases at https://crypto.bi

"""

Copyright (C) 2021 - crypto.bi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

Help support this Open Source project!
Donations address: X-avax1qr6yzjykcjmeflztsgv6y88dl0xnlel3chs3r4
Thank you!

"""

# --#--#--

from typing import List
import hashlib

HashLen = 32
RipeLen = 20
AddrLen = 20
Hash256 = [0] * HashLen
Hash160 = [0] * RipeLen

errBadLength = Exception("input has insufficient length")

def ComputeHash256Array(buf: bytes) -> bytes:
    """ComputeHash256Array Compute a cryptographically strong 256 bit hash of the input byte slice."""
    m = hashlib.sha256()    
    
    
    m.update(buf)
    return m.digest()    

def ComputeHash256(buf: bytes) -> bytes:
    """ComputeHash256 Compute a cryptographically strong 256 bit hash of the input byte slice."""
    return ComputeHash256Array(buf)
	

def ByteArraysToHash256Array(byteArray: List[bytes]) -> bytes:
    """ByteArraysToHash256Array takes in byte arrays and outputs a fixed 32 length byte array for the hash"""
    buffer = bytearray()
    for b in byteArray:
        buffer.extend(b)

    return ComputeHash256Array(bytes(buffer))


def ComputeHash256Ranges(buf: bytes, ranges: List[List[int]]) -> bytes:
    """ComputeHash256Ranges Compute a cryptographically strong 256 bit hash of the input byte slice in the ranges specified.
    Example: ComputeHash256Ranges({1, 2, 4, 8, 16}, {{1, 2}, {3, 5}}) is equivalent to ComputeHash256({2, 8, 16}).
    """
    m = hashlib.sha256()
    for r in ranges:
        m.update(buf[r[0]:r[1]])

    return m.digest()

def ComputeHash160Array(buf: bytes) -> bytes:
    """ComputeHash160Array Compute a cryptographically strong 160 bit hash of the input byte slice."""
    return ToHash160(ComputeHash160(buf))	

def ComputeHash160(buf: bytes) -> bytes:
    """ComputeHash160 Compute a cryptographically strong 160 bit hash of the input byte slice."""
    ripe = hashlib.new('ripemd160')
    ripe.update(buf)	
    return ripe.digest()

def Checksum(bbytes: bytes, length: int) -> bytes:
    """Checksum Create checksum of [length] bytes from the 256 bit hash of the byte slice.
    Returns the lower [length] bytes of the hash
    Errors if length > 32."""
    hash = ComputeHash256Array(bbytes)
    return hash[len(hash)-length:]


def ToHash256(bbytes: bytes) -> bytes:    
    if len(bbytes) != HashLen:
        raise errBadLength
        
    return bbytes


def ToHash160(bbytes: bytes) -> bytes:
	if len(bytes) != RipeLen:
		raise errBadLength
	
	return bbytes

def PubkeyBytesToAddress(key: bytes) -> bytes:
	return ComputeHash160(ComputeHash256(key))

