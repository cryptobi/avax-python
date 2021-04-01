#!/usr/bin/python3

# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

# Scratch pad. You can mostly ignore these scripts. Used for temporary testing of random stuff.

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--

from avaxpython.network.codec import Codec
from avaxpython.utils.wrappers.Packer import Packer
from avaxpython.network.Messages import Messages
from avaxpython.network.Op import Op

messages = [
    [0x01, 0x00, 0x00, 0x00, 0x01, 0xf7, 0xcb, 0xfb,
     0xc5, 0x00, 0x00, 0x00, 0x00, 0x60, 0x64, 0x65,
     0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x00, 0x00, 0xff, 0xff, 0xc0, 0xa8, 0x01,
     0xf1, 0x25, 0xb3, 0x00, 0x0f, 0x61, 0x76, 0x61,
     0x6c, 0x61, 0x6e, 0x63, 0x68, 0x65, 0x2f, 0x31,
     0x2e, 0x33, 0x2e, 0x31],
     bytearray.fromhex('0d0427d4b22a2a78bcddd456742caf91b56badbff985ee19aef14573e7343fd652ffffffff2ccf6bab9890026b5646b2266b2a12b995d08cdc31f87af05207bd48458ab48000000295f90292f9021aa08ec445d627f07413218ba7a086fd7a1d7d512e898a1adf6a51de010b6bd9b9c3a01dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347940100000000000000000000000000000000000000a0c191253eb7fef0caf14d934abee3b186a27c4ebabcdb2324790a9a195cd2ed01a042832900dc345daeb36f6b84879c94abdd619c1e532feb3ec3c5a3871be03c70a0056b23fbba480696b65fe5a59b8f2148a1299103c4f57df839233af2cf4ca2d2b901000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001830d4264837a1200825208846064967f80a00000000000000000000000000000000000000000000000000000000000000000880000000000000000a056e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421f870f86e80856d6e2edc008252089427854a16ab3154fb8d8c52fdba67063ec86f5072872386f26fc1000080830150f8a02f456012877664d75995a6ee397f23c4cd3a9e17c35eaa01f9549e7918fc4ceea007fe8345b396e371686330ea2fd9d7fbf05692332d61a4666e6ed5edba2cdac1c08080'),
]

for msg_bytes in messages:
    parsed_msg = Codec.Parse(bytes(msg_bytes))
    print(parsed_msg)
