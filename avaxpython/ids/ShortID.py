# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


from . import ID

class ShortID:
    """160 bit ID"""
    __AVAX_SHORTID_LENGTH = 20

    def __init__(self, bts: bytes = None):
        if bts is None:
            self.bytes = bytearray([0] * ShortID.__AVAX_SHORTID_LENGTH)
        else:

            if len(bts) != ShortID.__AVAX_SHORTID_LENGTH:
                raise Exception(f"Invalid ShortID byte length {len(bts)}. Expected {ShortID.__AVAX_SHORTID_LENGTH} bytes.")

            self.bytes = bts


    def __repr__(self) -> str:
        return self.bytes.hex()


