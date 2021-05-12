#!/usr/bin/python3
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

import json
from avaxpython.types import *
from avaxpython.codec.reflectcodec.type_codec import genericCodec

test_bytes = bytes([0,0,0,0,0,0,0,0])

class TopClass:
    _avax_tags = [
        ("tc", { "size": 2, "serializeV0": True, "serialize": True, "json": "tc" }),
    ]

    def __init__(self) -> None:
        self.tc = Uint16(22)
        self.ignore = Int32(1234)

    def __str__(self):
        _s = {
            "tc": str(self.tc),
            "ignore": str(self.ignore)
        }        
        return json.dumps(_s)

class SimpleClass:
    _avax_tags = [
		("a", { "size": 2, "serializeV0": True, "serialize": True, "json": "a" }),
		("b", { "size": 4, "serializeV0": True, "serialize": True, "json": "b" }),
        ("tclass", { "serializeV0": True, "serialize": True, "json": "tclass" }),
    ]

    def __init__(self) -> None:
        self.a = Uint16(99)
        self.b = Int32(1234)
        self.tclass = TopClass()

    def __str__(self):
        _s = {
            "a": str(self.a),
            "b": str(self.b),
            "tc": str(self.tclass.tc)
        }        
        return json.dumps(_s)

sc = SimpleClass()

assert(sc.a == 99)
assert(sc.b == 1234)
assert(sc.tclass.tc == 22)

genericCodec.Unmarshal(test_bytes, sc)

assert(sc.a == 0)
assert(sc.b == 0)
assert(sc.tclass.tc == 0)

print(f"OK : {sc}")
