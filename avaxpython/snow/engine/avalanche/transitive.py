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
from avaxpython.snow.engine.avalanche.bootstrap.bootstrapper import Bootstrapper
from avaxpython.snow.engine.common.engine import Engine
from avaxpython.ids.ShortID import ShortID
from avaxpython.ids.ID import ID

class Transitive(Bootstrapper, Engine):
    
    def __init__(self, vm, ctx, manager):
        Bootstrapper.__init__(self)
        Engine.__init__(self, ctx)
        self.VM = vm
        self.Manager = manager

    def Initialize(self, config):
        self.Manager = config.Manager

    def Gossip(self):
        """Gossip consensus messages with the network."""        

    def Shutdown(self):
        """Shut this consensus engine down"""        

    def Get(self, vdr: ShortID, requestID: int, vtxID: ID):
        """If this engine has access to the requested vertex, provide it"""

    def GetAncestors(self, vdr: ShortID, requestID: int, vtxID: ID):
        """Get ancestors for a given vertex"""

    def Put(self, vdr: ShortID, requestID: int, vtxID: ID, vtxBytes: bytes):
        vtx = self.Manager.ParseVtx(vtxBytes)
        handler = avaxpython.config().get("handler").consensus_handler
        handler.handle_vertex(vtx)
        
    def GetFailed(self, vdr: ShortID, requestID: int):
        """"""

    def PullQuery(self, vdr: ShortID, requestID: int, vtxID: ID):
        """"""

    def PushQuery(self, vdr: ShortID, requestID: int, vtxID: ID, vtxBytes: bytes):
        """"""

    def Chits(self, vdr: ShortID, requestID: int, votes: List[ID]):
        """"""

    def QueryFailed(self, vdr: ShortID, requestID: int):
        """"""

    def Notify(self, msg):
        """"""

    def GetVtx(self, vtxID: ID):
        """"""

    def GetVM(self):
        return self.VM
