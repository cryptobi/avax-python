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


from .Op import Op
from .Field import Field

class Msg:

    def __init__(self, op, fields, data_bytes):
        self.op = op 
        self.fields = fields
        self.bytes = data_bytes


    def __repr__(self) -> str:

        field_desc = {}
        for f in self.fields:
            k = "{}({})".format(Field.String(f), f)
            field_desc[k] = self.fields[f]

        dct = {
            'op': self.op,
            'op_name': Op.String(self.op),
            'fields': field_desc,
            'msg_size': len(self.bytes),
            'bytes': self.bytes.hex()
        }

        return "network.Msg " + str(dct)


    # Field returns the value of the specified field in this message
    def Op(self):
        return self.op 


    # Field returns the value of the specified field in this message
    def Get(self, field):
        return self.fields[field]


    # Bytes returns this message in bytes
    def Bytes(self):
        return self.bytes

        
