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

from typing import Dict
from avaxpython.codec.codec import Codec
from avaxpython.utils.wrappers.Packer import Packer
from avaxpython.codec.reflectcodec.type_codec import genericCodec

# default max size, in bytes, of something being marshalled by Marshal()
defaultMaxSize = 1 << 18

# initial capacity of byte slice that values are marshaled into.
# Larger value --> need less memory allocations but possibly have allocated but unused memory
# Smaller value --> need more memory allocations but more efficient use of allocated memory
initialSliceCap = 128


errMarshalNil        = Exception("can't marshal null pointer or interface")
errUnmarshalNil      = Exception("can't unmarshal null data")
errCantPackVersion   = Exception("couldn't pack codec version")
errCantUnpackVersion = Exception("couldn't unpack codec version")
errUnknownVersion    = Exception("unknown codec version")
errDuplicatedVersion = Exception("duplicated codec version")


class Manager:
    """Manager describes the functionality for managing codec versions."""

    def __init__(self, maxSize=defaultMaxSize, codecs=Dict[int, Codec]) -> None:
        self.maxSize = maxSize
        self.codecs: Dict[int, Codec] = {}
	
    def RegisterCodec(self, version: int, codec):
        """Associate the given codec with the given version ID"""
        pass

    def SetMaxSize(self, int):
        """	Define the maximum size, in bytes, of something serialized/deserialized
	    by this codec manager"""
        pass
	
    def Marshal(self, version: int, source):
        """Marshal the given value using the codec with the given version.
	    RegisterCodec must have been called with that version."""
        pass

    def Unmarshal(self, source: bytes, dest, type_ids={}):
        """	Unmarshal the given bytes into the given destination. [destination] must
	    be a pointer or an interface. Returns the version of the codec that
	    produces the given bytes."""
        if dest is None:
            raise errUnmarshalNil

        if source is None:
            raise errUnmarshalNil

        if len(source) > self.maxSize:            
            raise IndexError(f"Byte array exceeds maximum length {self.maxSize}")
        
        p = Packer(b=source)
        version = p.UnpackShort()

        # TODO implement codec versioning. NOP to keep pylint happy.
        version = version # punt

        if p.Errored():
            raise errCantUnpackVersion        

        return genericCodec.Unmarshal(p.Bytes[p.Offset:], dest, type_ids=type_ids)

