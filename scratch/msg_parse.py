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
]

for msg_bytes in messages:
    parsed_msg = Codec.Parse(bytes(msg_bytes))
    print(parsed_msg)
