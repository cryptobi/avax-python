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


from ..version import version
from avaxpython.utils import constants
from avaxpython.utils.logging import logger
from avaxpython.utils import logging
from avaxpython.ids.ShortID import ShortID
from avaxpython.ids.ID import ID
from avaxpython.network import network, upgrader
from avaxpython.network.tls.Config import Config as TLSConfig
from avaxpython.Config import Config as AppConf
from avaxpython.node.Config import Config as NodeConf
from avaxpython.errors import errors

TCP = "tcp"
genesisHashKey = b"genesisID"
Version                 = version.NewDefaultVersion(constants.PlatformName, 1, 1, 1)
versionParser           = version.NewDefaultParser()
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
        if err != nil:
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

    def __init__(self):

        self.Log = logger.Logger()
        self.LogFactory = logging.Factory()
        self.HTTPLog = logger.Logger()

        # This node's unique ID used when communicating with other nodes
        # (in consensus, for example)
        self.ID = ShortID()

        # Storage for this node
        # TODO DB = database.Database()

        # Handles calls to Keystore API
        # TODO keystoreServer = keystore.Keystore()

        # Manages shared memory
        # TODO sharedMemory = atomic.Memory()

        # Monitors node health and runs health checks
        # TODO healthService = health.CheckRegisterer()

        # Manages creation of blockchains and routing messages to them
        # TODO chainManager = chains.Manager()

        # Manages Virtual Machines
        # TODO vmManager = vms.Manager()

        # dispatcher for events as they happen in consensus
        # TODO DecisionDispatcher  = triggers.EventDispatcher()
        # TODO ConsensusDispatcher = triggers.EventDispatcher()

        # TODO IPCs *ipcs.ChainIPCs

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
        # TODO shuttingDown = utils.AtomicBool()

        # Incremented only once on initialization.
        # Decremented when node is done shutting down.
        # TODO doneShuttingDown = sync.WaitGroup()

        # Restarter can shutdown and restart the node
        # TODO restarter = utils.Restarter()


    def initNetworking(self):

        self.listener = None # TODO net.Listen(TCP, fmt.Sprintf(":%d", self.Config.StakingIP.Port))        
        self.dialer = None # TODO network.NewDialer(TCP)

        serverUpgrader = None
        clientUpgrader = None

        if self.Config.EnableP2PTLS:
            self.tlsConfig = TLSConfig(self.Config.StakingCertFile, self.Config.StakingKeyFile)
            serverUpgrader = upgrader.NewTLSServerUpgrader(self.tlsConfig)
            clientUpgrader = upgrader.NewTLSClientUpgrader(self.tlsConfig)
        else:
            serverUpgrader = upgrader.NewIPUpgrader()
            clientUpgrader = upgrader.NewIPUpgrader()
        
        # TODO validation not yet implemented. passive node.
        # Initialize validator manager and primary network's validator set
        # primaryNetworkValidators = validators.NewSet()
        # self.vdrs = validators.NewManager()
        # err = self.vdrs.Set(constants.PrimaryNetworkID, primaryNetworkValidators)
        # if  err != nil :
        #     return err
        
        """ TODO
        consensusRouter = self.Config.ConsensusRouter
        if not self.Config.EnableStaking :
            err = primaryNetworkValidators.AddWeight(n.ID, self.Config.DisabledStakingWeight)
            if  err != nil :
                return err
            
            consensusRouter = insecureValidatorManager(
                Router = consensusRouter,
                vdrs = primaryNetworkValidators,
                weight = self.Config.DisabledStakingWeight,
            )
        

        bootstrapWeight = self.beacons.Weight()
        reqWeight = (3 * bootstrapWeight + 3) / 4

        if reqWeight > 0 :
            # Set a timer that will fire after a given timeout unless we connect
            # to a sufficient portion of stake-weighted nodes. If the timeout
            # fires, the node will shutdown.
            def _f1():
                # If the timeout fires and we're already shutting down, nothing to do.
                if not self.shuttingDown.GetValue():
                    self.Log.Warn("Failed to connect to bootstrap nodes. Node shutting down...")
                    # TODO go  self.Shutdown()

            timer = timer.NewTimer(f1)

            # TODO go  timer.Dispatch()
            timer.SetTimeoutIn(beaconConnectionTimeout)

            consensusRouter = beaconManager(
                Router = consensusRouter,
                timer = timer,
                beacons = self.beacons,
                requiredWeight = reqWeight
            )
        """
        self.Net = network.NewDefaultNetwork(
            None, # TODO self.Config.ConsensusParams.Metrics,
            self.Log,
            self.ID,
            None, # TODO self.Config.StakingIP,
            None, # TODO self.Config.NetworkID,
            Version,
            versionParser,
            None, # TODO listener,
            None, # TODO dialer,
            serverUpgrader,
            clientUpgrader,
            None, # TODO primaryNetworkValidators,
            self.beacons,
            None, # TODO consensusRouter,
            None, # TODO self.Config.ConnMeterResetDuration,
            None, # TODO self.Config.ConnMeterMaxConns,
            None, # TODO self.restarter,
            None, # TODO self.Config.RestartOnDisconnected,
            None, # TODO self.Config.DisconnectedCheckFreq,
            None, # TODO self.Config.DisconnectedRestartTimeout,
            None, # TODO self.Config.ApricotPhase0Time,
            None, # TODO self.Config.SendQueueSize,
        )

        # syscall.SIGINT, syscall.SIGTERM
        def signal_handler():
            self.Shutdown()
            
        # TODO self.nodeCloser = # utils.HandleSignals(func(os.Signal) {
            # errors are already logged internally if they are meaningful
            
        

    # Dispatch starts the node's servers.
    # Returns when the node exits.
    def Dispatch(self):

        # Start the HTTP API server
        # TODO go  self.Log.RecoverAndPanic(func() {
        # TODO api server
        #if self.Config.HTTPSEnabled :
            #self.Log.Debug("initializing API server with TLS")
            #err = self.APIServer.DispatchTLS(n.Config.HTTPSCertFile, self.Config.HTTPSKeyFile)
            #self.Log.Warn("TLS enabled API server dispatch failed with %s. Attempting to create insecure API server", err)
        

        # self.Log.Debug("initializing API server without TLS")
        # err = self.APIServer.Dispatch() # TODO api server

        # When [n].Shutdown() is called, [n.APIServer].Close() is called.
        # This causes [n.APIServer].Dispatch() to return an error.
        # If that happened, don't log/return an error here.
        #if not self.shuttingDown.GetValue():
         #   self.Log.Fatal("API server dispatch failed with %s", err)

        # If the API server isn't running, shut down the node.
        # If node is already shutting down, this does nothing.
        #self.Shutdown()
        # })

        # Add bootstrap nodes to the peer network
        for _, peer in self.Config.BootstrapPeers:
            if not peer.IP.Equal(n.Config.StakingIP.IP()):
                self.Net.Track(peer.IP)
            else:
                self.Log.Error("can't add self as a bootstrapper")

        # Start P2P connections
        err = self.Net.Dispatch()

        # If the P2P server isn't running, shut down the node.
        # If node is already shutting down, this does nothing.
        self.Shutdown()

        # Wait until the node is done shutting down before returning
        self.doneShuttingDown.Wait()
        return err


    def initDatabase(self):
        self.DB = self.Config.DB

        expectedGenesis, _, err = genesis.Genesis(n.Config.NetworkID)
        if err != nil:
            return err

        rawExpectedGenesisHash = hashing.ComputeHash256(expectedGenesis)

        rawGenesisHash, err = self.DB.Get(genesisHashKey)
        if err == database.ErrNotFound :
            rawGenesisHash = rawExpectedGenesisHash
            err = self.DB.Put(genesisHashKey, rawGenesisHash)

        if err != nil:
            return err


        genesisHash, err = ids.ToID(rawGenesisHash)
        if err != nil:
            return err

        expectedGenesisHash, err = ids.ToID(rawExpectedGenesisHash)
        if err != nil:
            return err


        if genesisHash != expectedGenesisHash :
            return fmt.Errorf("db contains invalid genesis hash. DB Genesis: %s Generated Genesis: %s", genesisHash, expectedGenesisHash)

        return nil


    # Initialize this node's ID
    # If staking is disabled, a node's ID is a hash of its IP
    # Otherwise, it is a hash of the TLS certificate that this node
    # uses for P2P communication
    def initNodeID(self):
        if not self.Config.EnableP2PTLS :
            arx = bytearray(n.Config.StakingIP.IP().String())
            sidx = hashing.ComputeHash160Array(arx)
            self.ID = ShortID(sidx)
            self.Log.Info("Set the node's ID to %s", self.ID)
            return nil


        stakeCert, err = ioutil.ReadFile(n.Config.StakingCertFile)
        if err != nil:
            return fmt.Errorf("problem reading staking certificate: %w", err)


        block, _ = pem.Decode(stakeCert)
        cert, err = x509.ParseCertificate(block.Bytes)
        if err != nil:
            return fmt.Errorf("problem parsing staking certificate: %w", err)

        self.ID, err = ids.ToShortID(hashing.PubkeyBytesToAddress(cert.Raw))
        if err != nil:
            return fmt.Errorf("problem deriving staker ID from certificate: %w", err)

        self.Log.Info("Set node's ID to %s", self.ID)
        return nil


    # Set the node IDs of the peers this node should first connect to
    def initBeacons(self):
        self.beacons = validators.NewSet()
        for _, peer in self.Config.BootstrapPeers:
            err = self.beacons.AddWeight(peer.ID, 1)
            if  err != nil :
                return err
            
        
        return nil        

    # Create the EventDispatcher used for hooking events
    # into the general process flow.
    def initEventDispatcher(self):
        self.DecisionDispatcher = triggers.EventDispatcher()
        self.DecisionDispatcher.Initialize(n.Log)

        self.ConsensusDispatcher = triggers.EventDispatcher()
        self.ConsensusDispatcher.Initialize(n.Log)

        return self.ConsensusDispatcher.Register("gossip", self.Net)


    def initIPCs(self):
        chainIDs = None # TODO make([]ids.ID, len(n.Config.IPCDefaultChainIDs))
        for i, chainID in self.Config.IPCDefaultChainIDs:
            id, err = ids.FromString(chainID)
            if err != nil:
                return err
            
            chainIDs[i] = id            

        # var  err error
        self.IPCs, err = ipcs.NewChainIPCs(n.Log, self.Config.IPCPath, self.Config.NetworkID, self.ConsensusDispatcher, self.DecisionDispatcher, chainIDs)
        return err


    # Initializes the Platform chain.
    # Its genesis data specifies the other chains that should
    # be created.
    def initChains(self, genesisBytes, avaxAssetID):
        self.Log.Info("initializing chains")

        # Create the Platform Chain
        self.chainManager.ForceCreateChain(chains.ChainParameters(ID=constants.PlatformChainID, SubnetID=constants.PrimaryNetworkID, GenesisData=genesisBytes,  VMAlias=platformvm.ID.String(), CustomBeacons=n.beacons))

        return nil


    # initAPIServer initializes the server that handles HTTP calls
    def initAPIServer(self):
        self.Log.Info("initializing API server")

        return self.APIServer.Initialize(
            self.Log,
            self.LogFactory,
            self.Config.HTTPHost,
            self.Config.HTTPPort,
            self.Config.APIRequireAuthToken,
            self.Config.APIAuthPassword,
        )


    # Create the vmManager, chainManager and register the following VMs:
    # AVM, Simple Payments DAG, Simple Payments Chain, and Platform VM
    # Assumes self.DB, self.vdrs all initialized (non-nil)
    def initChainManager(self, avaxAssetID):
        self.vmManager = vms.NewManager(n.APIServer, self.HTTPLog)

        createAVMTx, err = genesis.VMGenesis(n.Config.NetworkID, avm.ID)
        if err != nil:
            return err

        xChainID = createAVMTx.ID()

        # If any of these chains die, the node shuts down
        criticalChains = ids.Set()
        criticalChains.Add(constants.PlatformChainID, createAVMTx.ID())

        # Set Prometheus metrics info
        self.Config.NetworkConfig.Namespace = constants.PlatformName
        self.Config.NetworkConfig.Registerer = self.Config.ConsensusParams.Metrics

        # Configure benchlist
        self.Config.BenchlistConfig.Validators = self.vdrs
        benchlistManager = benchlist.NewManager(n.Config.BenchlistConfig)

        # Manages network timeouts
        timeoutManager = timeout.Manager()
        err = timeoutManager.Initialize(n.Config.NetworkConfig, benchlistManager)
        if  err != nil :
            return err

        # TODO go  self.Log.RecoverAndPanic(timeoutManager.Dispatch)

        # Routes incoming messages from peers to the appropriate chain
        self.Config.ConsensusRouter.Initialize(
            self.ID,
            self.Log,
            timeoutManager,
            self.Config.ConsensusGossipFrequency,
            self.Config.ConsensusShutdownTimeout,
            criticalChains,
            self.Shutdown,
        )

        self.chainManager = chains.New(chains.ManagerConfig(StakingEnabled=n.Config.EnableStaking,
		MaxPendingMsgs = self.Config.MaxPendingMsgs,
		MaxNonStakerPendingMsgs = self.Config.MaxNonStakerPendingMsgs,
		StakerMSGPortion = self.Config.StakerMSGPortion,
		StakerCPUPortion = self.Config.StakerCPUPortion,
		Log = self.Log,
		LogFactory = self.LogFactory,
		VMManager = self.vmManager,
		DecisionEvents = self.DecisionDispatcher,
		ConsensusEvents = self.ConsensusDispatcher,
		DB = self.DB,
		Router = self.Config.ConsensusRouter,
		Net = self.Net,
		ConsensusParams = self.Config.ConsensusParams,
		EpochFirstTransition = self.Config.EpochFirstTransition,
		EpochDuration = self.Config.EpochDuration,
		Validators = self.vdrs,
		NodeID = self.ID,
		NetworkID = self.Config.NetworkID,
		Server = self.APIServer,
		Keystore = self.keystoreServer,
		AtomicMemory = self.sharedMemory,
		AVAXAssetID = avaxAssetID,
		XChainID = xChainID,
		CriticalChains = criticalChains,
		TimeoutManager = timeoutManager,
		HealthService = self.healthService,
		WhitelistedSubnets = self.Config.WhitelistedSubnets))

        vdrs = self.vdrs

        # If staking is disabled, ignore updates to Subnets' validator sets
        # Instead of updating node's validator manager, platform chain makes changes
        # to its own local validator manager (which isn't used for sampling)
        if not self.Config.EnableStaking :
            vdrs = validators.NewManager()


        # Register the VMs that Avalanche supports
        errs = wrappers.Errs()
        errs.Add(
            self.vmManager.RegisterVMFactory(platformvm.ID, platformvm.Factory(ChainManager =       self.chainManager,
			Validators =         vdrs,
			StakingEnabled =     self.Config.EnableStaking,
			CreationFee =        self.Config.CreationTxFee,
			Fee =                self.Config.TxFee,
			UptimePercentage =   self.Config.UptimeRequirement,
			MinValidatorStake =  self.Config.MinValidatorStake,
			MaxValidatorStake =  self.Config.MaxValidatorStake,
			MinDelegatorStake =  self.Config.MinDelegatorStake,
			MinDelegationFee =   self.Config.MinDelegationFee,
			MinStakeDuration =   self.Config.MinStakeDuration,
			MaxStakeDuration =   self.Config.MaxStakeDuration,
			StakeMintingPeriod = self.Config.StakeMintingPeriod,
			ApricotPhase0Time =  self.Config.ApricotPhase0Time)),
            self.vmManager.RegisterVMFactory(avm.ID, avm.Factory(CreationFee= self.Config.CreationTxFee, Fee=  self.Config.TxFee)),
            self.vmManager.RegisterVMFactory(evm.ID, rpcchainvm.Factory(Path=   filepath.Join(n.Config.PluginDir, "evm"), Config = self.Config.CorethConfig,)),
            self.vmManager.RegisterVMFactory(timestampvm.ID, timestampvm.Factory()),
            self.vmManager.RegisterVMFactory(secp256k1fx.ID, secp256k1fx.Factory()),
            self.vmManager.RegisterVMFactory(nftfx.ID, nftfx.Factory()),
            self.vmManager.RegisterVMFactory(propertyfx.ID, propertyfx.Factory()),
        )
        if errs.Errored():
            return errs.Err


        # Notify the API server when new chains are created
        self.chainManager.AddRegistrant(n.APIServer)
        return nil


    # initSharedMemory initializes the shared memory for cross chain interation
    def initSharedMemory(self):
        self.Log.Info("initializing SharedMemory")
        sharedMemoryDB = prefixdb.New(bytearray("shared memory"), self.DB)
        return self.sharedMemory.Initialize(n.Log, sharedMemoryDB)


    # initKeystoreAPI initializes the keystore service, which is an on-node wallet.
    # Assumes self.APIServer is already set
    def initKeystoreAPI(self):
        self.Log.Info("initializing keystore")
        keystoreDB = prefixdb.New(bytearray("keystore"), self.DB)
        err = self.keystoreServer.Initialize(n.Log, keystoreDB)
        if  err != nil :
            return err

        keystoreHandler, err = self.keystoreServer.CreateHandler()
        if err != nil:
            return err

        if not self.Config.KeystoreAPIEnabled :
            self.Log.Info("skipping keystore API initialization because it has been disabled")
            return nil

        self.Log.Info("initializing keystore API")
        return self.APIServer.AddRoute(keystoreHandler, sync.RWMutex(), "keystore", "", self.HTTPLog)


    # initMetricsAPI initializes the Metrics API
    # Assumes self.APIServer is already set
    def initMetricsAPI(self):
        registry, handler = metrics.NewService()
        # It is assumed by components of the system that the Metrics interface is
        # non-nil. So, it is set regardless of if the metrics API is available or not.
        self.Config.ConsensusParams.Metrics = registry
        if not self.Config.MetricsAPIEnabled :
            self.Log.Info("skipping metrics API initialization because it has been disabled")
            return nil


        self.Log.Info("initializing metrics API")

        dbNamespace = fmt.Sprintf("%s_db", constants.PlatformName)
        db, err = meterdb.New(dbNamespace, registry, self.DB)
        if err != nil:
            return err

        self.DB = db

        return self.APIServer.AddRoute(handler, sync.RWMutex(), "metrics", "", self.HTTPLog)


    # initAdminAPI initializes the Admin API service
    # Assumes self.log, self.chainManager, and self.ValidatorAPI already initialized
    def initAdminAPI(self):
        if not self.Config.AdminAPIEnabled :
            self.Log.Info("skipping admin API initialization because it has been disabled")
            return nil

        self.Log.Info("initializing admin API")
        service, err = admin.NewService(n.Log, self.chainManager, self.APIServer)
        if err != nil:
            return err

        return self.APIServer.AddRoute(service, sync.RWMutex(), "admin", "", self.HTTPLog)


    def initInfoAPI(self):
        if not self.Config.InfoAPIEnabled :
            self.Log.Info("skipping info API initialization because it has been disabled")
            return nil

        self.Log.Info("initializing info API")
        service, err = info.NewService(
            self.Log,
            Version,
            self.ID,
            self.Config.NetworkID,
            self.chainManager,
            self.Net,
            self.Config.CreationTxFee,
            self.Config.TxFee,
        )
        if err != nil:
            return err

        return self.APIServer.AddRoute(service, sync.RWMutex(), "info", "", self.HTTPLog)


    # initHealthAPI initializes the Health API service
    # Assumes self.Log, self.Net, self.APIServer, self.HTTPLog already initialized
    def initHealthAPI(self):
        if not self.Config.HealthAPIEnabled:
            self.healthService = health.NewNoOpService()
            self.Log.Info("skipping health API initialization because it has been disabled")
            return nil


        self.Log.Info("initializing Health API")
        service = health.NewService(n.Log)
        err = service.RegisterHeartbeat("network.validators.heartbeat", self.Net, 5*time.Minute)
        if  err != nil :
            return fmt.Errorf("couldn't register heartbeat health check: %w", err)

        def _ibf():
            pChainID, err = self.chainManager.Lookup("P")
            if  err != nil :
                return nil, errors.New("P-Chain not created")
            elif not self.chainManager.IsBootstrapped(pChainID):
                return nil, errors.New("P-Chain not bootstrapped")

            xChainID, err = self.chainManager.Lookup("X")
            if  err != nil :
                return nil, errors.New("X-Chain not created")
            elif not self.chainManager.IsBootstrapped(xChainID):
                return nil, errors.New("X-Chain not bootstrapped")

            cChainID, err = self.chainManager.Lookup("C")
            if  err != nil :
                return nil, errors.New("C-Chain not created")
            elif not self.chainManager.IsBootstrapped(cChainID):
                return nil, errors.New("C-Chain not bootstrapped")

            return nil, nil

        isBootstrappedFunc = _ibf
            

        # Passes if the P, X and C chains are finished bootstrapping
        err = service.RegisterMonotonicCheckFunc("chains.default.bootstrapped", isBootstrappedFunc)
        if  err != nil :
            return err

        handler, err = service.Handler()
        if err != nil:
            return err

        self.healthService = service
        return self.APIServer.AddRoute(handler, sync.RWMutex(), "health", "", self.HTTPLog)


    # initIPCAPI initializes the IPC API service
    # Assumes self.log and self.chainManager already initialized
    def initIPCAPI(self):
        if not self.Config.IPCAPIEnabled :
            self.Log.Info("skipping ipc API initialization because it has been disabled")
            return nil

        self.Log.Info("initializing ipc API")
        service, err = ipcsapi.NewService(n.Log, self.chainManager, self.APIServer, self.IPCs)
        if err != nil:
            return err

        return self.APIServer.AddRoute(service, sync.RWMutex(), "ipcs", "", self.HTTPLog)


    # Give chains and VMs aliases as specified by the genesis information
    def initAliases(self, genesisBytes):
        self.Log.Info("initializing aliases")
        defaultAliases, chainAliases, vmAliases, err = genesis.Aliases(genesisBytes)
        if err != nil:
            return err


        for chainID, aliases in chainAliases:
            for _, alias in aliases:
                err = self.chainManager.Alias(chainID, alias)
        if  err != nil :
                    return err



        for vmID, aliases in vmAliases:
            for _, alias in aliases:
                err = self.vmManager.Alias(vmID, alias)
        if  err != nil :
                    return err



        for url, aliases in defaultAliases:
            err = self.APIServer.AddAliases(url, aliases)
        if  err != nil :
                return err


        return nil


    # Initialize this node
    def Initialize(self, config, logger, logFactory, restarter):
        self.Log = logger
        self.LogFactory = logFactory
        self.Config = config
        self.restarter = restarter
        self.doneShuttingDown.Add(1)
        self.Log.Info("Node version is: %s", Version)

        httpLog, err = logFactory.MakeSubdir("http")
        if err != nil:
            return fmt.Errorf("problem initializing HTTP logger: %w", err)

        self.HTTPLog = httpLog

        err = self.initDatabase()
        if  err != nil : # Set up the node's database
            return fmt.Errorf("problem initializing database: %w", err)

        err = self.initNodeID()
        if  err != nil : # Derive this node's ID
            return fmt.Errorf("problem initializing staker ID: %w", err)

        err = self.initBeacons()
        if  err != nil : # Configure the beacons
            return fmt.Errorf("problem initializing node beacons: %w", err)

        # Start HTTP APIs
        err = self.initAPIServer()
        if  err != nil : # Start the API Server
            return fmt.Errorf("couldn't initialize API server: %w", err)

        err = self.initKeystoreAPI()
        if  err != nil : # Start the Keystore API
            return fmt.Errorf("couldn't initialize keystore API: %w", err)

        err = self.initMetricsAPI()
        if  err != nil : # Start the Metrics API
            return fmt.Errorf("couldn't initialize metrics API: %w", err)


        err = self.initSharedMemory()
        if  err != nil : # Initialize shared memory
            return fmt.Errorf("problem initializing shared memory: %w", err)


        err = self.initNetworking()
        if  err != nil : # Set up all networking
            return fmt.Errorf("problem initializing networking: %w", err)

        err = self.initEventDispatcher()
        if  err != nil : # Set up the event dipatcher
            return fmt.Errorf("problem initializing event dispatcher: %w", err)

        genesisBytes, avaxAssetID, err = genesis.Genesis(n.Config.NetworkID)
        if err != nil:
            return fmt.Errorf("couldn't create genesis bytes: %w", err)

        # Start the Health API
        # Has to be initialized before chain manager
        err = self.initHealthAPI()
        if  err != nil :
            return fmt.Errorf("couldn't initialize health API: %w", err)

        err = self.initChainManager(avaxAssetID)
        if  err != nil : # Set up the chain manager
            return fmt.Errorf("couldn't initialize chain manager: %w", err)

        err = self.initAdminAPI()
        if  err != nil : # Start the Admin API
            return fmt.Errorf("couldn't initialize admin API: %w", err)

        err = self.initInfoAPI()
        if  err != nil : # Start the Info API
            return fmt.Errorf("couldn't initialize info API: %w", err)

        err = self.initIPCs()
        if  err != nil : # Start the IPCs
            return fmt.Errorf("couldn't initialize IPCs: %w", err)

        err = self.initIPCAPI()
        if  err != nil : # Start the IPC API
            return fmt.Errorf("couldn't initialize the IPC API: %w", err)

        err = self.initAliases(genesisBytes)
        if  err != nil : # Set up aliases
            return fmt.Errorf("couldn't initialize aliases: %w", err)

        err = self.initChains(genesisBytes, avaxAssetID)
        if  err != nil : # Start the Platform chain
            return fmt.Errorf("couldn't initialize chains: %w", err)

        return nil


    # Shutdown this node
    # May be called multiple times
    def Shutdown(self):
        self.shuttingDown.SetValue(true)
        self.shutdownOnce.Do(n.shutdown)


    def shutdown(self):
        self.Log.Info("shutting down node")
        if self.IPCs != nil :
            err = self.IPCs.Shutdown()
            if  err != nil :
                self.Log.Debug("error during IPC shutdown: %s", err)


        if self.chainManager != nil :
            self.chainManager.Shutdown()

        if self.Net != nil :
            # Close already logs its own error if one occurs, so the error is ignored here
            _ = self.Net.Close()

        err = self.APIServer.Shutdown()
        if  err != nil :
            self.Log.Debug("error during API shutdown: %s", err)

        utils.ClearSignals(n.nodeCloser)
        self.doneShuttingDown.Done()
        self.Log.Info("finished node shutdown")

