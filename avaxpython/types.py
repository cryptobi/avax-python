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

import numpy as np

Uint8 = np.uint8
Int8 = np.int8
Uint16 = np.uint16
Int16 = np.int16
Uint32 = np.uint32
Int32 = np.int32
Uint64 = np.uint64
Int64 = np.int64
Bool = np.bool
String = str
Interface = type(object)
Struct = type(object)
Ptr = type(object)
Invalid = None
Bytes = bytes
Byte = Uint8

class Slice(list):
    pass

class Array(list):
    def __init__(self, arr=None):
        if arr:
            self.arr = arr
        else:
            self.arr = []

class ByteSlices:
    """Wrapper for an array of slices"""
    def __init__(self, slices = None) -> None:
        self.slices = slices

    def __struct__(self):
        slices = self.slices
        if slices:
            slices = [ba.hex() for ba in self.slices]        
        else:
            slices = []
        _s = {
            'ByteSlices' : {
                'slices' : slices
            }
        }
        return _s


    def __str__(self):
        if self.slices:
            _d = { "slices": [f"{len(_s)} Bytes" for _s in self.slices] }
            return str(_d)
        else:
            return "Empty ByteSlices"
        

class ByteArrays:
    """
        Wrapper for an array of byte arrays. Needed to store array size.

        :param array_size - Number of elements in each array.
    """
    def __init__(self, arrays = None, array_size = 0) -> None:
        if arrays:
            self.arrays = arrays
        else:
            self.arrays = []

        self.array_size = array_size

    def __struct__(self):
        _s = {
            'ByteArrays' : {
                'arrays' : [ba.hex() for ba in self.arrays]
            }
        }
        return _s

    def __str__(self):
        if self.arrays:
            _d = { 
                "array_size" : self.array_size, 
                "arrays": f"[{len(self.arrays)} Arrays]"
            }
            return str(_d)
        else:
            return "Empty ByteArrays"
        

