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

# Until we implement dynamic chain creation, this helper maps chain IDs.

from avaxpython.chains.chain import chain
from avaxpython.snow.context import Context
from avaxpython.snow.engine.avalanche.transitive import Transitive as AVMTransitive
from avaxpython.snow.engine.snowman.transitive import Transitive as SnowTransitive
from avaxpython.snow.networking.router.handler import Handler
from avaxpython.snow.networking.router.dummy_handler import DummyHandler
from avaxpython.utils.constants import application
from avaxpython.utils import constants
from avaxpython.chains.chain_parameters import ChainParameters
from avaxpython.chains.manager_config import ManagerConfig
from avaxpython.vms import platformvm, evm, avm, timestampvm, secp256k1fx, nftfx, propertyfx, rpcchainvm
from avaxpython.utils import constants
from avaxpython.main.params import Config as MainConfig
from avaxpython.snow.engine.avalanche.state.serializer import Serializer

# General -------------------------------------------------------------------------------------

beacons = []

P_id = "11111111111111111111111111111111LpoYY"
P_name = "P"
X_id = "2oYMBNV4eNHyqk2fjjV5nVQLDbtmNJzq5s3qs3Lo6ftnC6FByM"
X_name = "X"
C_id = "2q9e4r6Mu3U68nU1fYjgbR6JvwrRx36CohpAX5UQxse55x1Q5"
C_name = "C"

chains = {}
VMManager = None
AVAXAssetID = None
ConsensusDispatcher = None
DecisionDispatcher = None
x_chain_id  = None
NodeID = None

def InitChains():

    global chains
    global NodeID
    global AVAXAssetID
    global ConsensusDispatcher
    global DecisionDispatcher
    global x_chain_id

    # P-Chain -------------------------------------------------------------------------------------

    P_vmID = "rWhpuQPF1kb72esV2momhMuTYGkEb1oL29pt2EBXWmSy4kxnT"
    P_chain_id_str = "11111111111111111111111111111111LpoYY"
    P_params = ChainParameters(
                idx=constants.PlatformChainID,
                subnet_id=constants.PrimaryNetworkID,
                genesis_data=bytes(),
                vm_alias=platformvm.ID.String(),
                custom_beacons=beacons,
                fx_aliases=[]
            )
    P_context = Context(
                    NetworkID =  constants.MainnetID,
                    SubnetID = P_params.SubnetID,
                    chain_id = P_params.ID,
                    NodeID = NodeID,
                    x_chain_id = x_chain_id,
                    AVAXAssetID = AVAXAssetID,
                    Log = None,
                    DecisionDispatcher = DecisionDispatcher,
                    ConsensusDispatcher = ConsensusDispatcher,
                    Keystore = None,
                    SharedMemory = None,
                    BCLookup = None,
                    SNLookup = None,
                    Namespace = f"avalanche_P_vm",
                    Metrics = None,
                    EpochFirstTransition = None,
                    EpochDuration = 0,
                )

    P_vmFactory = VMManager.GetVMFactory(P_vmID)
    P_vm = P_vmFactory.New(P_context)
    P_engine = SnowTransitive(P_vm, P_context)
    P_handler = Handler(ctx=P_context, engine=P_engine)
    P_handler.Initialize(P_engine, None, None, None, None, None, None, "avalanche_P_handler", None, None)
    P_beacons = []

    # X-Chain -------------------------------------------------------------------------------------

    X_vmID = "jvYyfQTxGMJLuGWa55kdP2p2zSUYsQ5Raupu4TW34ZAUBAbtq"
    X_chain_id_str = "2oYMBNV4eNHyqk2fjjV5nVQLDbtmNJzq5s3qs3Lo6ftnC6FByM"
    X_params = ChainParameters(
                idx=X_chain_id_str,
                subnet_id=constants.PrimaryNetworkID,
                genesis_data=bytes(),
                vm_alias=avm.ID.String(),
                custom_beacons=beacons,
                fx_aliases=[]
            )
    X_context = Context(
                    NetworkID =  constants.MainnetID,
                    SubnetID = X_params.SubnetID,
                    chain_id = X_params.ID,
                    NodeID = NodeID,
                    x_chain_id = x_chain_id,
                    AVAXAssetID = AVAXAssetID,
                    Log = None,
                    DecisionDispatcher = DecisionDispatcher,
                    ConsensusDispatcher = ConsensusDispatcher,
                    Keystore = None,
                    SharedMemory = None,
                    BCLookup = None,
                    SNLookup = None,
                    Namespace = f"avalanche_X_vm",
                    Metrics = None,
                    EpochFirstTransition = None,
                    EpochDuration = 0,
                )

    X_vmFactory = VMManager.GetVMFactory(X_vmID)
    X_vm = X_vmFactory.New(X_context)
    vtx_manager = Serializer(X_context, X_vm, None, None, None)
    X_engine = AVMTransitive(X_vm, X_context, manager = vtx_manager)
    X_handler = Handler(ctx=X_context, engine=X_engine)
    X_handler.Initialize(X_engine, None, None, None, None, None, None, "avalanche_X_handler", None, None)
    X_beacons = []

    # C-Chain -------------------------------------------------------------------------------------

    C_vmID = "mgj786NP7uDwBCcq6YwThhaN8FLyybkCa4zBWTQbNgmK6k9A6"
    C_chain_id_str = "2q9e4r6Mu3U68nU1fYjgbR6JvwrRx36CohpAX5UQxse55x1Q5"
    C_params = ChainParameters(
                idx=C_chain_id_str,
                subnet_id=constants.PrimaryNetworkID,
                genesis_data=bytes(),
                vm_alias=avm.ID.String(),
                custom_beacons=beacons,
                fx_aliases=[]
            )
    C_context = Context(
                    NetworkID =  constants.MainnetID,
                    SubnetID = C_params.SubnetID,
                    chain_id = C_params.ID,
                    NodeID = NodeID,
                    x_chain_id = x_chain_id,
                    AVAXAssetID = AVAXAssetID,
                    Log = None,
                    DecisionDispatcher = DecisionDispatcher,
                    ConsensusDispatcher = ConsensusDispatcher,
                    Keystore = None,
                    SharedMemory = None,
                    BCLookup = None,
                    SNLookup = None,
                    Namespace = f"avalanche_C_vm",
                    Metrics = None,
                    EpochFirstTransition = None,
                    EpochDuration = 0,
                )

    C_vmFactory = VMManager.GetVMFactory(C_vmID)
    C_vm = P_vmFactory.New(C_context)
    C_engine = SnowTransitive(C_vm, C_context)
    C_handler = DummyHandler(ctx=C_context, engine=C_engine)
    C_handler.Initialize(C_engine, None, None, None, None, None, None, "avalanche_C_handler", None, None)
    C_beacons = []

    chains = { 
            # P-Chain
            P_id: chain(
                P_name, 
                P_engine, 
                P_handler, 
                P_context, 
                P_vm, 
                P_beacons, 
                P_params
            ), 
            # X-Chain
            X_id: chain(
                X_name, 
                X_engine, 
                X_handler, 
                X_context, 
                X_vm, 
                X_beacons, 
                X_params
            ),
            #C-Chain
            C_id: chain(
                C_name, 
                C_engine, 
                C_handler, 
                C_context, 
                C_vm, 
                C_beacons, 
                C_params            
            ),
    }

