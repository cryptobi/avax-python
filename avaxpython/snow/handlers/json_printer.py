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
import avaxpython
from avaxpython.snow.handlers.handler import Handler
from avaxpython.snow.consensus.avalanche.vertex import Vertex
from avaxpython.snow.consensus.snowman.block import Block


class JSONPrinter(Handler):
    """
        Handles consensus messages by printing them out in JSON format.
        Vertices and Blocks passed to the handler must inherit AvaxStructured.
    """
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def extract_struct(t):

        if not t:
            return None

        if "__struct__" in dir(t):
            _s = t.__struct__()
            for k, v in _s.items():
                _s[k] = str(v)

            return _s

        else:
            return t

    def handle_vertex(self, vtx: Vertex):
        """Handle DAG vertex messages."""
        _s = JSONPrinter.extract_struct(vtx)
        avaxpython.config().logger().debug("***********************")
        avaxpython.config().logger().debug("*** VERTEX RECEIVED ***")
        avaxpython.config().logger().debug("***********************")
        avaxpython.config().logger().debug(json.dumps(_s))

    def handle_block(self, blk: Block):
        """Handle Block messages."""   
        _s = JSONPrinter.extract_struct(blk)
        avaxpython.config().logger().debug("**********************")
        avaxpython.config().logger().debug("*** BLOCK RECEIVED ***")
        avaxpython.config().logger().debug("**********************")
        avaxpython.config().logger().debug(json.dumps(_s))
