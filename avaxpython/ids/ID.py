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

from avaxpython.types import *
from avaxpython.utils.formatting.encoding import Encoding

defaultEncoding = Encoding.CB58

class ID:

    """Avalanche uses two ID sizes: 256 bit ID (32 bytes) and 160 bit (20 bytes).
    This class implements the 256 bit ID's.
    An Avalanche ID is defined as type ID [32]byte in avalanchego/ids/id.go
    We've wrapped the bytes and constants in a Python class.
    """

    __AVAX_ID_LENGTH = 32

    _avax_tags = [
        ("bytes", { "size": 32, "json": "version", "serializeV0": True, "serialize": True }),
    ]

    def __init__(self, bts: Bytes = None):

        if bts is None:
            self.bytes = Bytes(bytearray([0] * ID.__AVAX_ID_LENGTH))
        else:

            if len(bts) > ID.__AVAX_ID_LENGTH:
                raise Exception(f"Invalid ID byte length {len(bts)}. Expected {ID.__AVAX_ID_LENGTH} bytes.")

            self.bytes = bytearray(bts)

            if len(self.bytes) < ID.__AVAX_ID_LENGTH:
                # If shorter, then pad ID with zeroes.
                self.bytes.extend([0] * (ID.__AVAX_ID_LENGTH-len(bts)))
                self.bytes = Bytes(self.bytes)

    def __str__(self):
        global defaultEncoding
        enc = Encoding(defaultEncoding)
        encoded = enc.Encode(self.bytes)
        return encoded

    def __repr__(self):
        return self.bytes.hex()

    def __eq__(self, id2):
        
        if len(self.bytes) != len(id2.bytes):
            return False

        for i in range(len(self.bytes)):
            if self.bytes[i] != id2.bytes[i]:
                return False

        return True

    def __hash__(self):
        return hash(bytes(self.bytes))

    def String(self):
        return self.__str__()
        