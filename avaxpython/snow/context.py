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

from avaxpython.ids.ID import ID
from avaxpython.ids.ShortID import ShortID

class Context:
    def __init__(self, NetworkID: int = 0, SubnetID: ID = ID(), chain_id: ID = ID(), NodeID: ShortID = ShortID(), x_chain_id: ID = ID(), AVAXAssetID:ID = ID(), 
                Log = None, DecisionDispatcher= None, ConsensusDispatcher = None, Lock = None, Keystore = None, SharedMemory = None, BCLookup = None, 
                SNLookup = None, Namespace: str = "", Metrics = None, EpochFirstTransition = None, EpochDuration = None, Clock = None, bootstrapped: int = 0):
        """Context is information about the current execution.
        [NetworkID] is the ID of the network this context exists within.
        [chain_id] is the ID of the chain this context exists within.
        [NodeID] is the ID of this node"""    
        self.NetworkID: int = NetworkID
        self.SubnetID: ID = SubnetID
        self.chain_id: ID = chain_id
        self.NodeID: ShortID = NodeID
        self.Xchain_id: ID = x_chain_id
        self.AVAXAssetID:ID = AVAXAssetID
        self.Log = Log
        self.DecisionDispatcher = DecisionDispatcher
        self.ConsensusDispatcher = ConsensusDispatcher
        self.Lock = Lock
        self.Keystore = Keystore
        self.SharedMemory = SharedMemory
        self.BCLookup = BCLookup
        self.SNLookup = SNLookup
        self.Namespace: str = Namespace
        self.Metrics = Metrics

        # Epoch management
        self.EpochFirstTransition = EpochFirstTransition
        self.EpochDuration = EpochDuration
        self.Clock = Clock

        # Non-zero iff this chain bootstrapped. Should only be accessed atomically.
        self.bootstrapped: int = bootstrapped
    
    def IsBootstrapped(ctx) -> bool:
        """IsBootstrapped returns true iff this chain is done bootstrapping"""
        return int(ctx.bootstrapped) > 0
    
    def Bootstrapped(ctx):
        """Bootstrapped marks this chain as done bootstrapping"""
        ctx.bootstrapped = 1
        
    def Epoch(ctx) -> int:
        """Epoch this context thinks it's in based on the wall clock time."""
        now = ctx.Clock.Time()
        timeSinceFirstEpochTransition = now.Sub(ctx.EpochFirstTransition)
        epochsSinceFirstTransition = timeSinceFirstEpochTransition / ctx.EpochDuration
        currentEpoch = epochsSinceFirstTransition + 1
        if currentEpoch < 0:
            return 0        

        return int(currentEpoch)
        

class EventDispatcher:
    def Issue(ctx : Context, containerID: ID, container: bytes):
        pass

    def Accept(ctx : Context, containerID: ID, container: bytes):
        pass

    def Reject(ctx : Context, containerID: ID, container: bytes):
        pass


class Keystore:
    def GetDatabase(username, password: str):
        pass


class AliasLookup:
    def Lookup(alias: str):
        pass

    def PrimaryAlias(idx: ID):
        pass


class SubnetLookup:
    def SubnetID(chain_id: ID):
        pass


class emptyEventDispatcher:

    def Issue(Context, ID, bbytes):
        pass

    def Accept(Context, ID, bbytes):
        pass

    def Reject(Context, ID, bbytes):
        pass
