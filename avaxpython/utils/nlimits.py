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


# Python C language limits, from https://stackoverflow.com/questions/52475749/maximum-and-minimum-value-of-c-types-integers-from-python

import sys

from ctypes import c_int8, c_uint8, c_byte, c_ubyte, c_int16, c_uint16, \
    c_int32, c_uint32, c_int, c_uint, c_long, c_ulong, c_longlong, c_ulonglong, \
    c_int64, c_uint64, \
    sizeof

def limits(c_int_type):
    signed = c_int_type(-1).value < c_int_type(0).value
    bit_size = sizeof(c_int_type) * 8
    signed_limit = 2 ** (bit_size - 1)
    return (-signed_limit, signed_limit - 1) if signed else (0, 2 * signed_limit - 1)

