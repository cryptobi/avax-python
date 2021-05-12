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

from typing import Dict
from avaxpython.ids.ID import ID
from avaxpython.ids.ShortID import ShortID
from avaxpython.snow.networking.router.handler import Handler
from avaxpython.utils import constants
from typing import List

class ChainRouter:

    def __init__(self, chains={}, peers=[]):
        self.chains : Dict[ID, Handler] = chains
        self.peers = peers

    def get_chain(self, chain_ID):

        chain_ID_str = str(chain_ID)     
        if chain_ID_str not in self.chains:
            raise RuntimeError(f"chain_id {chain_ID_str} not handled by this Router.")

        return self.chains[chain_ID_str]

    def Shutdown(self):
        pass

    def GetAcceptedFrontier(self, validator_id: ShortID, chain_id: ID, request_id: int, deadline: int):
        pass
    
    def AcceptedFrontier(self, validator_id: ShortID, chain_id: ID, request_id: int, containerIDs: List[ID]):
        pass

    def GetAcceptedFrontierFailed(self, validator_id: ShortID, chain_id: ID, request_id: int):
        pass
    
    def GetAccepted(self, validator_id: ShortID, chain_id: ID, request_id: int, deadline: int, containerIDs: List[ID]):
        pass    

    def Accepted(self, validator_id: ShortID, chain_id: ID, request_id: int, containerIDs: List[ID]):
        pass

    def GetAcceptedFailed(self, validator_id: ShortID, chain_id: ID, request_id: int):
        pass

    def GetAncestors(self, validator_id: ShortID, chain_id: ID, request_id: int, deadline: int, containerID: ID):
        pass

    def MultiPut(self, validator_id: ShortID, chain_id: ID, request_id: int, containers: List[bytes]):
        pass

    def GetAncestorsFailed(self, validator_id: ShortID, chain_id: ID, request_id: int):
        pass

    def Get(self, validator_id: ShortID, chain_id: ID, request_id: int, deadline: int, containerID: ID):
        chain = self.get_chain(chain_id)        
        chain.Get(validator_id, request_id, containerID, containerID)

    def Put(self, validator_id, chain_id, request_id, containerID, container):
        chain = self.get_chain(chain_id)        
        chain.Put(validator_id, request_id, containerID, container)

    def GetFailed(self, validator_id: ShortID, chain_id: ID, request_id: int):
        pass

    def AddChain(self, handler: Handler):
        """AddChain registers the specified chain so that incoming messages can be routed to it"""
        
        chain_id: ID = handler.Context().chain_id        
        self.chains[str(chain_id)] = handler        

        for validator_id in self.peers:
            handler.Connected(validator_id)            
	
    def RemoveChain(self, chain_id: ID):
        """RemoveChain removes the specified chain so that incoming messages can't be routed to it"""
        
        if chain_id not in self.chains:
            return

        chain = self.chains[chain_id]        
        del self.chains[chain_id]
        chain.Shutdown()

    def PushQuery(self, validator_id: ShortID, chain_id: ID, request_id: int, deadline: int, containerID : ID, container: bytes):
        pass

    def PullQuery(self, validator_id: ShortID, chain_id: ID, request_id: int, deadline: int, containerID: ID):
        pass

    def Chits(self, validator_id: ShortID, chain_id: ID, request_id: int, votes: List[ID]):
        pass

    def QueryFailed(self, validator_id: ShortID, chain_id: ID, request_id: int):
        pass

    def Connected(self, validator_id: ShortID):
        pass    

    def Disconnected(self, validator_id: ShortID):
        pass    

    def Gossip(self):
        pass    

    def EndInterval(self):
        pass    

    def HealthCheck(self):
        pass    

