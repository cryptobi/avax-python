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

from avaxpython.types import Bytes
from avaxpython.ids.ID import ID

class ShortID:
    """160 bit ID"""
    __AVAX_SHORTID_LENGTH = 20

    _avax_tags = [
        ("bytes", { "size": __AVAX_SHORTID_LENGTH, "json": "version", "serialize": True }),
    ]


    def __init__(self, bts: bytes = None):
        if bts is None:
            self.bytes = Bytes(bytearray([0] * ShortID.__AVAX_SHORTID_LENGTH))
        else:

            if len(bts) != ShortID.__AVAX_SHORTID_LENGTH:
                raise Exception(f"Invalid ShortID byte length {len(bts)}. Expected {ShortID.__AVAX_SHORTID_LENGTH} bytes.")

            self.bytes = Bytes(bts)


    def __str__(self) -> str:
        return self.bytes.hex()


    def __repr__(self) -> str:
        return self.bytes.hex()

    def __hash__(self):
        return hash(bytes(self.bytes))

    def String(self):
        """Utility method to preserve Go code interface"""
        return str(self)
