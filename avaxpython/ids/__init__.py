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


import hashlib
from avaxpython.ids.ID import ID
from avaxpython.ids.ShortID import ShortID
from avaxpython.utils.formatting.encoding import Encoding

defaultEncoding = Encoding.defaultEncoding

def Empty():
    return ID()

def ToShortID(bts: bytes) -> bytes:
    n = hashlib.new('ripemd160')
    n.update(bts)    
    return ShortID(n.digest())


def ToID(bts: bytes) -> bytes:
    n = hashlib.new('sha256')
    n.update(bts)
    return ID(n.digest())



def FromString(idStr: str) -> ID:
    """FromString is the inverse of ID.String()"""
    bbytes = formatting.Decode(defaultEncoding, idStr)
    if bbytes is None:
        raise Exception("Error decoding string to ID")
    return ToID(bbytes)
