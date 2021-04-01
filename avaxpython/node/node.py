# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


import json
import time
import random
import avaxpython
from ..version import version
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from avaxpython.utils import constants
from avaxpython.utils.logging import logger
from avaxpython.utils import logging
from avaxpython.utils.ip import IPDesc
from avaxpython.ids.ShortID import ShortID
from avaxpython.network.network import Network
from avaxpython.ids.ID import ID
from avaxpython.genesis import beacons
from avaxpython.network import network, upgrader, dialer
from avaxpython.network.peer import Peer
from avaxpython.network.tls.Config import Config as TLSConfig
from avaxpython.Config import Config as AppConf
from avaxpython.node.Config import Config as NodeConf
from avaxpython.errors import errors
from avaxpython.wallet import BIP32
from avaxpython import ids
from avaxpython.network.Builder import Builder
from avaxpython.vms.manager import Manager as ChainManager


TCP = "tcp"
genesisHashKey = b"genesisID"
Version = version.NewDefaultVersion(constants.PlatformName, 1, 1, 1)
versionParser = version.NewDefaultParser()
beaconConnectionTimeout = 1 * 60

class insecureValidatorManager:

    def __init__(self):
        self.router = router.Router()
        self.vdrs =  validators.Set()
        self.weight = 0        

    def Connected(vdrID):
        i.vdrs.AddWeight(vdrID, i.weight)
        i.Router.Connected(vdrID)

    def Disconnected(vdrID):
        i.vdrs.RemoveWeight(vdrID, i.weight)
        i.Router.Disconnected(vdrID)        


class beaconManager:

    def __init__(self):
        self.router = router.Router()
        self.timer = timer.Timer
        self.beacons = validators.Set()
        self.requiredWeight = 0
        self.weight = 0

    def Connected(self, vdrID):
        weight, ok = b.beacons.GetWeight(vdrID)
        if not ok :
            b.Router.Connected(vdrID)
            return
        
        weight, err = math.Add64(weight, b.weight)
        if err != None:
            b.timer.Cancel()
            b.Router.Connected(vdrID)
            return
        
        b.weight = weight
        if b.weight >= b.requiredWeight :
            b.timer.Cancel()
        
        b.Router.Connected(vdrID)
    

    def Disconnected(vdrID):
        weight, ok = b.beacons.GetWeight(vdrID)
        if  ok :
            # TODO: Account for weight changes in a more robust manner.

            # Sub64 should rarely error since only validators that have added their
            # weight can become disconnected. Because it is possible that there are
            # changes to the validators set, we utilize that Sub64 returns 0 on
            # error.
            b.weight, _ = math.Sub64(b.weight, weight)
        
        self.Router.Disconnected(vdrID)
        

# Node is an instance of an Avalanche node.
class Node:

    def __init__(self, avax_config=None):

        self.Log = logger.Logger()
        self.LogFactory = logging.Factory()
        self.HTTPLog = logger.Logger()

        # This node's unique ID used when communicating with other nodes
        # (in consensus, for example)
        self.ID = ShortID()

        # Net runs the networking stack
        self.Net = None # network.Network()

        # this node's initial connections to the network
        self.beacons = None # validators.Set()

        # current validators of the network
        self.vdrs = None # validators.Manager()

        # Handles HTTP API calls
        # TODO APIServer = api.Server()

        # This node's configuration
        self.Config = NodeConf()

        # channel for closing the node
        self.nodeCloser = None # chan<- os.Signal

        # ensures that we only close the node once.
        # TODO shutdownOnce = sync.Once()

        # True if node is shutting down or is done shutting down
        self.shuttingDown = False

        # Incremented only once on initialization.
        # Decremented when node is done shutting down.
        self.doneShuttingDown = False

        # Restarter can shutdown and restart the node
        # TODO restarter = utils.Restarter()


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
    
        
        self.Net = Network(avax_config = self.avax_config)
        self.Net.listener = network.listener(None, self.Config.StakingIP.Port)        
        self.Net.dialer = dialer.NewDialer(self.avax_config)
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

            p = Peer(self.Net, conn = None, ip = IPDesc(host_addr, int(host_port)), port = int(host_port), node = self, avax_config=self.avax_config)

            self.Config.BootstrapPeers.append(p)

        for peer in self.Config.BootstrapPeers:
            if peer.ip.IP != self.Config.StakingIP.IP:
                self.Net.track(peer)
                pass
            else:
                self.Log.Error("can't add self as a bootstrapper")

        while True:          
            for fut in self.Net.futures:      
                print(fut)

            time.sleep(5)                

        self.Net.Dispatch()
        
        # If the P2P server isn't running, shut down the node.
        # If node is already shutting down, this does nothing.
        self.Shutdown()

        # Wait until the node is done shutting down before returning
        self.doneShuttingDown.Wait()
        return err


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

    # Initialize this node's ID
    # If staking is disabled, a node's ID is a hash of its IP
    # Otherwise, it is a hash of the TLS certificate that this node
    # uses for P2P communication
    def initNodeID(self):

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
        self.beacons = {}
        for peer in self.Config.BootstrapPeers:
            self.beacons.AddWeight(peer.ID, 1)            
            

    # Create the EventDispatcher used for hooking events
    # into the general process flow.
    def initEventDispatcher(self):
        pass


    # Initializes the Platform chain.
    # Its genesis data specifies the other chains that should
    # be created.
    def initChains(self, genesisBytes: bytes):
        pass


    # initAPIServer initializes the server that handles HTTP calls
    def initAPIServer(self):
        pass


    # Create the vmManager, chainManager and register the following VMs:
    # AVM, Simple Payments DAG, Simple Payments Chain, and Platform VM
    # Assumes self.DB, self.vdrs all initialized (non-nil)
    def initChainManager(self, avaxAssetID):
        self.vmManager = ChainManager()



    # initSharedMemory initializes the shared memory for cross chain interation
    def initSharedMemory(self):
        pass


    # initKeystoreAPI initializes the keystore service, which is an on-node wallet.
    # Assumes self.APIServer is already set
    def initKeystoreAPI(self):
        pass


    # initMetricsAPI initializes the Metrics API
    # Assumes self.APIServer is already set
    def initMetricsAPI(self):
        pass


    # initAdminAPI initializes the Admin API service
    # Assumes self.log, self.chainManager, and self.ValidatorAPI already initialized
    def initAdminAPI(self):
        pass


    def initInfoAPI(self):
        pass


    # initHealthAPI initializes the Health API service
    # Assumes self.Log, self.Net, self.APIServer, self.HTTPLog already initialized
    def initHealthAPI(self):
        pass


    # initIPCAPI initializes the IPC API service
    # Assumes self.log and self.chainManager already initialized
    def initIPCAPI(self):
        pass


    # Give chains and VMs aliases as specified by the genesis information
    def initAliases(self, genesisBytes):
        pass


    def Initialize(self, config, avax_config):
        
        self.Config = config
        self.avax_config = avax_config
        self.Version = self.avax_config.get("version")
        self.Config.StakingCertFile = self.avax_config.get("staker_crt")
        self.Log = avax_config.logger()
        self.doneShuttingDown = False
        self.Log.info(f"Node version is: {self.Version}")
        self.initNodeID()
        self.initBeacons()
        self.initNetworking()
        self.initChainManager(self.Config.AvaxAssetID)
        


    def Shutdown(self):
        self.shuttingDown = True
        self.shutdown()


    def shutdown(self):
        self.Log.info("Running node Shutdown routine.")

        if self.Net is not None:
            self.Net.Close()
                        
        self.Log.info("Finished node Shutdown()")

