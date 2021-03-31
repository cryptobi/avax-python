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
from .Messages import Messages
from avaxpython.utils.wrappers.Packer import Packer
from avaxpython.network.Msg import Msg
from avaxpython.network.Field import Field

# Codec defines the serialization and deserialization of network messages
class Codec:

    # Pack attempts to pack a map of fields into a message.
    # The first byte of the message is the opcode of the message.
    @staticmethod
    def Pack(op, fields):
        message = Messages.get(op)

        if not message:
            return None

        p = Packer(b"")
        p.PackByte(op)

        for field in message:
            data = fields[field]

            if data is None:
                raise Exception(f"Message op {op} missing field {field}")
            
            packer = Field.Packer(field)

            if not packer:
                    raise Exception(f"Packer not found for field {field}")

            packer(p, data)

        
        return Msg(op, fields, p.Bytes)


    # Parse attempts to convert bytes into a message.
    # The first byte of the message is the opcode of the message.
    @staticmethod
    def Parse(msg: bytes):

        opcode = msg[0]
        fields = {}

        msg_fields = Messages.get(opcode)
        packer = Packer(msg)
        packer.Offset = 1

        for field in msg_fields:
            unpacker = Field.Unpacker(field)
            if not unpacker:
                raise Exception(f"Unpacker not found for field {field}")

            fields[field] = unpacker(packer)

        return Msg(opcode, fields, msg)
