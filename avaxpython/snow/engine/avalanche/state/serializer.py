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

from avaxpython.snow.engine.avalanche.state import unique_vertex
from avaxpython.snow.engine.avalanche.vertex.parser import Parser


dbCacheSize = 10000
idCacheSize = 1000

errUnknownVertex = Exception("unknown vertex")
errWrongChainID  = Exception("wrong ChainID in vertex")


class Serializer:

    def __init__(self, ctx, vm, state, db, edge):
        self.ctx = ctx
        self.vm = vm
        self.state = state
        self.db = db
        self.edge = edge

    def Initialize(sef, ctx, vm, db):
        pass

    def ParseVtx(self, b: bytes):
        return unique_vertex.newUniqueVertex(self, b)

    def parseVertex(self, b: bytes):            
        vtx = Parser.Parse(b)
        return vtx 

    def Build(self):
        pass

    # Get implements the avalanche.State interface
    def Get(self, vtxID):
        return self.getVertex(vtxID) 

    # Edge implements the avalanche.State interface
    def Edge(self): 
        return self.edge.List()

    def getVertex(self, vtxID):

        vtx = uniqueVertex(serializer = s, vtxID = vtxID)

        if vtx.Status() == choices.Unknown:
            raise errUnknownVertex
        
        return vtx

