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

from avaxpython.ids.ID import ID
from avaxpython.utils.hashing import hashing

errNilMetadata           = Exception("nil metadata is not valid")
errMetadataNotInitialize = Exception("metadata was never initialized and is not valid")


class Metadata:
    def __init__(self) -> None:        
        self.id: ID  = None # The ID of this data
        self.unsignedBytes: bytes = None # Unsigned byte representation of this data
        self.bytes: bytes = None # Byte representation of this data

    def Initialize(self, unsignedBytes: bytes, bbytes: bytes):
        """Initialize set the bytes and ID"""
        self.id = hashing.ComputeHash256Array(bbytes)
        self.unsignedBytes = unsignedBytes
        self.bytes = bbytes

    
    def ID(self) -> ID:
        """ID returns the unique ID of this data"""
        return self.id
    
    def UnsignedBytes(self) -> bytes:
        """UnsignedBytes returns the unsigned binary representation of this data"""
        return self.unsignedBytes

    def Bytes(self) -> bytes:
        """Bytes returns the binary representation of this data"""
        return self.bytes
    
    def Verify(self):
        """Verify implements the verify.Verifiable interface"""
        if self.id == ids.Empty:
            return errMetadataNotInitialize
        else:
            return None
