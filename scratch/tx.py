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
from avaxpython.snow.engine.avalanche.vertex.stateless_vertex import innerStatelessVertex
from avaxpython.codec.reflectcodec.type_codec import genericCodec
from avaxpython.utils.wrappers.Packer import Packer
from avaxpython.vms.avm.tx import Tx
from avaxpython.vms.avm.types import registered_types
from avaxpython.utils.formatting.encoding import Encoding

txbytes = bytearray.fromhex("00000000000300000001ed5f38341e436e5d46e2bb00b45d62ae97d1b050c64bc634ae10626739e35c4b0000000121e67317cbc4be2aeb00677ad6462778a8f52274b9d605df2591b23027a87dff00000007000000520ef23eef00000000000000000000000100000001107bb6b9ae55ce54d6e83602b55699ebea87e0150000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a8d7f87f1c8a5583c1ca92b20b8ace3330ba0d9ddaa7f4bfa6435f75459f73940000000021e67317cbc4be2aeb00677ad6462778a8f52274b9d605df2591b23027a87dff00000005000000520f01812f0000000100000000000000010000000900000001cf929996c66224fb7f3dafc3916ee0b1c64070ff472f325a3e976db8a346d6fa20ae77ca53ddf5d36a5bf629d3359ad79cfed1217cfe33710663be738f5d785300")

enc = Encoding()
txID = enc.HashEncode(txbytes)
print(f"TX ID {txID}")

p = Packer(txbytes)	
b = p.UnpackShort()
print(f"Codec Version: {b}")
tx = Tx()
dest = genericCodec._unmarshal(p, tx, type_ids=registered_types)

print("\n\n\n")
print(dest)
print("\n\n\n")