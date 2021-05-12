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
from avaxpython.utils.hashing import hashing
from avaxpython.snow.consensus.snowstorm.tx import Tx as SnowstormTx
from avaxpython.utils.formatting.encoding import Encoding

class vertexState:

    def __init__(self, unique=None, vtx=None, status=None, parents=None, txs=None) -> None:        
        self.unique: bool = unique
        self.vtx = vtx
        self.status = status
        self.parents = parents
        self.txs = txs

    def __struct__(self):

        txs = self.txs
        if self.txs and "__dict__" in self.txs:
            if "__struct__" in self.txs.__dict__:
                txs = self.txs.__dict__()

        vtx = self.vtx
        if vtx and "__struct__" in dir(vtx):
            vtx = vtx.__struct__()

        return { 'VertexState': {
                "unique" : self.unique,
                "vtx": vtx,
                "status": self.status,
                "parents": self.parents,
                "txs": txs
            }            
        }


class uniqueVertex:
    """uniqueVertex acts as a cache for vertices in the database.

    If a vertex is loaded, it will have one canonical uniqueVertex. The vertex
    will eventually be evicted from memory, when the uniqueVertex is evicted from
    the cache. If the uniqueVertex has a function called again afther this
    eviction, the vertex will be re-loaded from the database.
    """
    def __init__(self, serializer, vtxid, vertex_state=vertexState()):

        self.serializer = serializer
        self.vtxID = vtxid
        self.v = vertex_state

    def Txs(self) -> List[SnowstormTx]:

        if self.v.vtx == None:
            raise RuntimeError(f"failed to get txs for undefined vertex")
        
        txs = []
        
        for tx_bytes in self.v.vtx.innerStatelessVertex.Txs.slices:
            tx = self.serializer.vm.ParseTx(tx_bytes)
            txs.append(tx)
        
        return txs

    def __struct__(self):
        enc = Encoding()
        vid = self.vtxID

        if isinstance(vid, bytes):
            vid = enc.Encode(vid)

        state = self.v
        if state:
            state = state.__struct__()

        return { 'UniqueVertex': {
                "vertex_id" : vid,
                "state": state,
                "txs" : self.Txs()
            }            
        }

    def __repr__(self):        
        return str(self.__struct__())


def newUniqueVertex(serializer, b: bytes):
    
    vtx = uniqueVertex(
        vtxid = hashing.ComputeHash256Array(b),
        serializer = serializer
    )
    
    vtx.v.vtx = serializer.parseVertex(b)

    return vtx
    