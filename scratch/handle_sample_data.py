#!/usr/bin/python3
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

# This is a dummy network-less node. 
# It handles messages read from local storage (e.g. sample-data/)
# Used for debugging / testing.


from avaxpython.handlers.DEFAULT import DefaultHandler
import avaxpython
from avaxpython.snow.handlers.json_printer import JSONPrinter
import os
import sys
import os.path
import random
import signal
import traceback
from avaxpython.ids.ShortID import ShortID
from avaxpython.Config import Config as AVAXConfig
from avaxpython.network.handlers.AVAX import AVAX as AVAXHandler
from avaxpython.network.network import Network
from avaxpython.utils.ip import IPDesc
from avaxpython.snow.networking.router.chain_router import ChainRouter
from avaxpython.network.peer import Peer
from avaxpython.chains.manager import Manager as ChainManager
from avaxpython.chains.chain_parameters import ChainParameters
from avaxpython.utils import constants
from avaxpython.vms import platformvm, evm, avm, timestampvm, secp256k1fx, nftfx, propertyfx, rpcchainvm
from avaxpython.vms.manager import Manager as VMManager
from avaxpython.chains import chain_configs
from avaxpython.snow.validators.manager import Manager as ValidatorsManager
from avaxpython.main import params
from avaxpython.vms.platformvm.factory import Factory as PVMFactory
from avaxpython.vms.avm.factory import Factory as AVMFactory
from avaxpython.vms.rpcchainvm.factory import Factory as RPCVMFactory
from avaxpython.vms.timestampvm.factory import Factory as TimestampVMFactory
from avaxpython.vms.secp256k1fx.factory import Factory as SECPVMFactory
from avaxpython.vms.nftfx.factory import Factory as NFTVMFactory
from avaxpython.vms.propertyfx.factory import Factory as PropertyVMFactory

if "AVAX_PYTHON_PATH" not in os.environ:
    print("Please set AVAX_PYTHON_PATH environment variable. Run . setenv.sh")
    exit(1)

data_dir = "{}/sample-data".format(os.environ['AVAX_PYTHON_PATH'])

if not os.path.exists(data_dir):
    print("Directory {} does not exist. Create it first.".format(data_dir))
    exit(1)

class DummyConnection:

    def send(self, b: bytes):
        return len(b)

def sigint_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

params.parseCmdLine()
node_config = params.Config

avaxpython.config().set("handler", DefaultHandler())

avax_handler = AVAXHandler()
network = Network(router=ChainRouter())
network.nodeID = random.randint(9999, 4294967295)
peer = Peer(network, DummyConnection(), IPDesc('127.0.0.1', 9651), None, 0, None, None, my_staking_ip=IPDesc('127.0.0.1', 9651))

chainManager = ChainManager()
dummy_node_id = ShortID()

vmManager = VMManager()
chain_configs.VMManager = vmManager

vdrs = ValidatorsManager()

chainManager = ChainManager()
chainManager.config.VMManager = vmManager
chainManager.config.Validators = vdrs
chainManager.config.Router = node_config.ConsensusRouter
chainManager.config.ConsensusParams = node_config.ConsensusParams

vmManager.RegisterVMFactory(platformvm.ID, PVMFactory(
    ChainManager=       chainManager,
    Validators=         vdrs,
    StakingEnabled=     node_config.EnableStaking,
    CreationFee=        node_config.CreationTxFee,
    Fee=                node_config.TxFee,
    UptimePercentage=   node_config.UptimeRequirement,
    MinValidatorStake=  node_config.MinValidatorStake,
    MaxValidatorStake=  node_config.MaxValidatorStake,
    MinDelegatorStake=  node_config.MinDelegatorStake,
    MinDelegationFee=   node_config.MinDelegationFee,
    MinStakeDuration=   node_config.MinStakeDuration,
    MaxStakeDuration=   node_config.MaxStakeDuration,
    StakeMintingPeriod= node_config.StakeMintingPeriod,
    ApricotPhase0Time=  node_config.ApricotPhase0Time,
)),
vmManager.RegisterVMFactory(avm.ID, AVMFactory(
    CreationFee= node_config.CreationTxFee,
    Fee=         node_config.TxFee,
)),
vmManager.RegisterVMFactory(evm.ID, RPCVMFactory(
    Path=   os.path.join(node_config.PluginDir, "evm"),
    Config= node_config.CorethConfig,
)),
vmManager.RegisterVMFactory(timestampvm.ID, TimestampVMFactory()),
vmManager.RegisterVMFactory(secp256k1fx.ID, SECPVMFactory()),
vmManager.RegisterVMFactory(nftfx.ID, NFTVMFactory()),
vmManager.RegisterVMFactory(propertyfx.ID, PropertyVMFactory()),


chainManager.ForceCreateChain(ChainParameters(
            idx=constants.PlatformChainID,
            subnet_id=constants.PrimaryNetworkID,
            genesis_data=b"",
            vm_alias=platformvm.ID.String(),
            custom_beacons=[],
            fx_aliases=[],
            node_id=dummy_node_id
        ))

for arr in os.walk(data_dir):
    for fil in arr[2]:
        path = "{}/{}".format(arr[0], fil)
        with open(path, "rb") as f:
            message = f.read()
            try:
                avax_handler.handle_msg(message, peer)
            except Exception as e:                
                print(f"\n\n\nERROR {e}")
                traceback.print_exc(file=sys.stdout)
                print("\n\n\n\a")
