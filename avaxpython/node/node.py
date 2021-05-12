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


import time
import random
import os.path
from ..version import version
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import avaxpython
from avaxpython.utils import constants
from avaxpython.utils.logging import logger
from avaxpython.utils import logging
from avaxpython.utils.ip import IPDesc
from avaxpython.ids.ShortID import ShortID
from avaxpython.network.network import Network
from avaxpython.ids.ID import ID
from avaxpython.genesis import beacons, aliases
from avaxpython.network import network, upgrader, dialer
from avaxpython.network.peer import Peer
from avaxpython.network.tls.Config import Config as TLSConfig
from avaxpython.Config import Config as AppConf
from avaxpython.node.Config import Config as NodeConfig
from avaxpython.errors import errors
from avaxpython.wallet import BIP32
from avaxpython import ids
from avaxpython.network.Builder import Builder
from avaxpython.vms.manager import Manager as VMManager
from avaxpython.chains.manager import Manager as ChainManager
from avaxpython.chains import manager
from avaxpython.vms import platformvm, evm, avm, timestampvm, secp256k1fx, nftfx, propertyfx, rpcchainvm
from avaxpython.vms.platformvm.factory import Factory as PVMFactory
from avaxpython.vms.avm.factory import Factory as AVMFactory
from avaxpython.vms.rpcchainvm.factory import Factory as RPCVMFactory
from avaxpython.vms.timestampvm.factory import Factory as TimestampVMFactory
from avaxpython.vms.secp256k1fx.factory import Factory as SECPVMFactory
from avaxpython.vms.nftfx.factory import Factory as NFTVMFactory
from avaxpython.vms.propertyfx.factory import Factory as PropertyVMFactory
from avaxpython.snow.validators.manager import Manager as ValidatorsManager
from avaxpython.chains.chain_parameters import ChainParameters
from avaxpython.chains import chain_configs
from avaxpython.utils.hashing import hashing
from avaxpython.snow.networking.router.chain_router import ChainRouter

TCP = "tcp"
genesisHashKey = b"genesisID"
Version = version.NewDefaultVersion(constants.PlatformName, 1, 1, 1)
versionParser = version.NewDefaultParser()
beaconConnectionTimeout = 1 * 60

class insecureValidatorManager:

    def __init__(self):
        self.Router = Router()
        self.vdrs =  set()
        self.weight = 0        

    def Connected(self, vdrID):
        self.vdrs.AddWeight(vdrID, self.weight)
        self.Router.Connected(vdrID)

    def Disconnected(self, vdrID):
        self.vdrs.RemoveWeight(vdrID, self.weight)
        self.Router.Disconnected(vdrID)        


class beaconManager:

    def __init__(self):
        self.Router = Router()
        self.timer = None
        self.beacons = set()
        self.requiredWeight = 0
        self.weight = 0

    def Connected(self, vdrID):
        weight, ok = self.beacons.GetWeight(vdrID)
        if not ok :
            self.Router.Connected(vdrID)
            return
        
        weight, err = math.Add64(weight, self.weight)
        if err != None:
            self.timer.Cancel()
            self.Router.Connected(vdrID)
            return
        
        self.weight = weight
        if self.weight >= self.requiredWeight :
            self.timer.Cancel()
        
        self.Router.Connected(vdrID)
    

    def Disconnected(self, vdrID):
        weight, ok = self.beacons.GetWeight(vdrID)
        if  ok :
            # TODO: Account for weight changes in a more robust manner.

            # Sub64 should rarely error since only validators that have added their
            # weight can become disconnected. Because it is possible that there are
            # changes to the validators set, we utilize that Sub64 returns 0 on
            # error.
            self.weight, _ = math.Sub64(b.weight, weight)
        
        self.Router.Disconnected(vdrID)
        

# Node is an instance of an Avalanche node.
class Node:

    def __init__(self, config=NodeConfig(), beacons=(), network=None):

        self.Log = logger.Logger()

        # This node's unique ID used when communicating with other nodes (in consensus, for example)
        self.ID = ShortID()

        # Net runs the networking stack
        self.Net: network.Network = network

        # this node's initial connections to the network
        self.beacons = beacons

        # current validators of the network
        self.vdrs = None # validators.Manager()

        # This node's configuration
        self.Config = config

        # True if node is shutting down or is done shutting down
        self.shuttingDown = False

        # Incremented only once on initialization.
        # Decremented when node is done shutting down.
        self.doneShuttingDown = False
        self.chainManager = ChainManager()


    def initNetworking(self):

        serverUpgrader = None
        clientUpgrader = None

        if self.Config.EnableP2PTLS:
            self.tlsConfig = TLSConfig(self.Config.StakingCertFile, self.Config.StakingKeyFile)
            serverUpgrader = upgrader.NewTLSServerUpgrader(self.tlsConfig)
            clientUpgrader = upgrader.NewTLSClientUpgrader(self.tlsConfig)
        else:
            serverUpgrader = upgrader.NewIPUpgrader()
            clientUpgrader = upgrader.NewIPUpgrader()
    
        
        consensusRouter = self.Config.ConsensusRouter

        self.Net = Network(router=consensusRouter)
        self.Net.listener = network.listener(None, self.Config.StakingIP.Port)        
        self.Net.dialer = dialer.NewDialer()
        self.Net.log = self.Log
        self.Net.serverUpgrader = serverUpgrader
        self.Net.clientUpgrader = clientUpgrader
        self.Net.beacons = self.beacons
        self.Net.b = Builder()
        self.Net.nodeID = random.randint(9999, 4294967295)


    # Dispatch starts the node's servers.
    # Returns when the node exits.
    def  Dispatch(self):

        for i in range(len(beacons.beacon_ips[constants.MainnetID])):

            beacon_hp = beacons.beacon_ips[constants.MainnetID][i]
            beacon_id = beacons.beacon_ids[constants.MainnetID][i]

            host_addr, host_port = beacon_hp.split(":")

            p = Peer(self.Net, conn = None, ip = IPDesc(host_addr, int(host_port)), port = int(host_port), node = self, my_staking_ip=self.Config.StakingIP)

            self.Config.BootstrapPeers.append(p)

        random.shuffle(self.Config.BootstrapPeers)
        for peer in self.Config.BootstrapPeers:
            if peer.ip.IP != self.Config.StakingIP.IP:
                self.Net.track(peer)
            else:
                self.Log.Error("can't add self as a bootstrapper")

        self.Net.Dispatch()
        
        # If the P2P server isn't running, shut down the node.
        # If node is already shutting down, this does nothing.
        self.Shutdown()

        # Wait until the node is done shutting down before returning
        self.doneShuttingDown.Wait()


    def initDatabase(self):
        pass

    def IDFromCert(self):
        with open(self.Config.StakingCertFile, "rb") as f:
            pem_data = f.read()
        
        cert = x509.load_pem_x509_certificate(pem_data, default_backend())
        if cert is None:
            return f"problem parsing staking certificate"

        p_key = cert.public_key()
        raw_pkey = p_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

        addr = BIP32.address_from_publickey_bytes(raw_pkey)
        self.ID = ids.ToShortID(addr)
        if self.ID == None:
            return f"problem deriving staker ID from certificate"

        return self.ID

    def initNodeID(self):
        """Initialize this node's ID
        If staking is disabled, a node's ID is a hash of its IP
        Otherwise, it is a hash of the TLS certificate that this node uses for P2P communication"""
        if not self.Config.EnableP2PTLS:
            arx = bytearray(n.Config.StakingIP.IP().String())
            sidx = hashing.ComputeHash160Array(arx)
            self.ID = ShortID(sidx)
            self.Log.info("Set the node's ID to %s", self.ID)
            return None

        self.IDFromCert()        
        self.Log.info("Set node ID to %s", self.ID)

        return self.ID

    def initBeacons(self):
        self.beacons = ()
        for peer in self.Config.BootstrapPeers:
            self.beacons.AddWeight(peer.ID, 1)            
            

    def initEventDispatcher(self):
        """Create the EventDispatcher used for hooking events into the general process flow."""        

    def initChains(self, genesisBytes: bytes):
        """Initializes the Platform chain.
        Its genesis data specifies the other chains that should be created."""        
        self.Log.info("Initializing Chains")

        # Create the Platform Chain
        self.chainManager.ForceCreateChain(ChainParameters(
            idx=constants.PlatformChainID,
            subnet_id=constants.PrimaryNetworkID,
            genesis_data=genesisBytes, # Specifies other chains to create
            vm_alias=platformvm.ID.String(),
            custom_beacons=self.beacons,
            fx_aliases=[],
            node_id=self.ID
        ))


    
    def initAPIServer(self):
        """initAPIServer initializes the server that handles HTTP calls"""
        pass


    def initChainManager(self, avaxAssetID):
        """Create the vmManager, chainManager and register the following VMs:
        AVM, Simple Payments DAG, Simple Payments Chain, and Platform VM
        Assumes self.DB, self.vdrs all initialized (non-nil)"""
        self.vmManager = VMManager()
        chain_configs.VMManager = self.vmManager

        vdrs = ValidatorsManager()

        self.chainManager = ChainManager()
        self.chainManager.config.VMManager = self.vmManager
        self.chainManager.config.Validators = vdrs
        self.chainManager.config.Router = self.Config.ConsensusRouter
        self.chainManager.config.ConsensusParams = self.Config.ConsensusParams

        self.vmManager.RegisterVMFactory(platformvm.ID, PVMFactory(
            ChainManager=       self.chainManager,
            Validators=         self.vdrs,
            StakingEnabled=     self.Config.EnableStaking,
            CreationFee=        self.Config.CreationTxFee,
            Fee=                self.Config.TxFee,
            UptimePercentage=   self.Config.UptimeRequirement,
            MinValidatorStake=  self.Config.MinValidatorStake,
            MaxValidatorStake=  self.Config.MaxValidatorStake,
            MinDelegatorStake=  self.Config.MinDelegatorStake,
            MinDelegationFee=   self.Config.MinDelegationFee,
            MinStakeDuration=   self.Config.MinStakeDuration,
            MaxStakeDuration=   self.Config.MaxStakeDuration,
            StakeMintingPeriod= self.Config.StakeMintingPeriod,
            ApricotPhase0Time=  self.Config.ApricotPhase0Time,
        )),
        self.vmManager.RegisterVMFactory(avm.ID, AVMFactory(
            CreationFee= self.Config.CreationTxFee,
            Fee=         self.Config.TxFee,
        )),
        self.vmManager.RegisterVMFactory(evm.ID, RPCVMFactory(
            Path=   os.path.join(self.Config.PluginDir, "evm"),
            Config= self.Config.CorethConfig,
        )),
        self.vmManager.RegisterVMFactory(timestampvm.ID, TimestampVMFactory()),
        self.vmManager.RegisterVMFactory(secp256k1fx.ID, SECPVMFactory()),
        self.vmManager.RegisterVMFactory(nftfx.ID, NFTVMFactory()),
        self.vmManager.RegisterVMFactory(propertyfx.ID, PropertyVMFactory()),

    
    def initSharedMemory(self):
        """initSharedMemory initializes the shared memory for cross chain interation"""


    def initKeystoreAPI(self):
        """initKeystoreAPI initializes the keystore service, which is an on-node wallet.
        Assumes self.APIServer is already set"""


    def initMetricsAPI(self):
        """initMetricsAPI initializes the Metrics API
        Assumes self.APIServer is already set"""


    def initAdminAPI(self):
        """initAdminAPI initializes the Admin API service
        Assumes self.log, self.chainManager, and self.ValidatorAPI already initialized
        """

    def initInfoAPI(self):
        """Initialize Info API"""

    def initHealthAPI(self):
        """initHealthAPI initializes the Health API service
        Assumes self.Log, self.Net, self.APIServer, self.HTTPLog already initialized"""

    def initIPCAPI(self):
        """initIPCAPI initializes the IPC API service
        Assumes self.log and self.chainManager already initialized"""

    def initAliases(self, genesisBytes):
        """Give chains and VMs aliases as specified by the genesis information"""
        defaultAliases, chainAliases, vmAliases = aliases.Aliases(genesisBytes)

        for chainID, l_aliases in chainAliases.items():
            for alias in l_aliases:
                self.chainManager.Alias(chainID, alias)

        for vmID, l_aliases in vmAliases.items():
            for alias in l_aliases:
                self.vmManager.Alias(vmID, alias)



    def Initialize(self, config):
        
        self.Config = config
        self.Version = avaxpython.config().get("version")
        self.AgentVersion = avaxpython.config().get("agent_version")
        self.Config.StakingCertFile = avaxpython.config().get("staker_crt")
        self.Log = avaxpython.config().logger()
        self.doneShuttingDown = False
        self.Log.info(f"Node version is: {self.Version}")
        self.Log.info(f"Agent version is: {self.AgentVersion}")
        self.initNodeID()
        self.initBeacons()
        self.initNetworking()
        self.initChainManager(self.Config.AvaxAssetID)
        self.initAliases(self.Config.GenesisBytes)
        self.initChains(self.Config.GenesisBytes)


    def Shutdown(self):
        self.shuttingDown = True

        self.Log.info("Running node Shutdown routine.")

        if self.Net is not None:
            self.Net.Close()
                        
        self.Log.info("Finished node Shutdown()")

