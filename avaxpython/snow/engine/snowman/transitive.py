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

from typing import List
import avaxpython
from avaxpython.snow.engine.common.engine import Engine
from avaxpython.snow.engine.snowman.bootstrap.bootstrapper import Bootstrapper
from avaxpython.ids.ShortID import ShortID
from avaxpython.ids.ID import ID


class Transitive(Engine, Bootstrapper):

    def __init__(self, vm, ctx):
        Engine.__init__(self, ctx)
        Bootstrapper.__init__(self, vm, ctx)
        self.VM = vm
        self.Ctx = ctx        

    def Initialize(self, config):
        """#TODO"""

    def Gossip(self):
        """#TODO"""

    def Shutdown(self):
        """#TODO"""

    def Get(self, vdr: ShortID, request_id: int, block_id: ID):
        """#TODO"""

    def GetAncestors(self, vdr: ShortID, request_id: int, block_id: ID):
        """#TODO"""

    def Put(self, vdr: ShortID, request_id: int, block_id: ID, block_bytes: bytes):
        blk = self.VM.ParseBlock(block_bytes)
        handler = avaxpython.config().get("handler").consensus_handler
        handler.handle_block(blk)

    def GetFailed(self, vdr: ShortID, request_id: int):
        """#TODO"""

    def PullQuery(self, vdr: ShortID, request_id: int, block_id: ID):
        """#TODO"""

    def PushQuery(self, vdr: ShortID, request_id: int, block_id: ID, block_bytes: bytes):
        """#TODO"""

    def Chits(self, vdr: ShortID, request_id: int, votes: List[ID]):
        """#TODO"""

    def QueryFailed(self, vdr: ShortID, request_id: int):
        """#TODO"""

    def Notify(self, msg):
        """#TODO"""

    def IsBootstrapped(self):
        """#TODO"""

    def HealthCheck(self):
        """#TODO"""

    def GetBlock(self, block_id: ID): 
        """#TODO"""

    def GetVM(self):
        """#TODO"""
