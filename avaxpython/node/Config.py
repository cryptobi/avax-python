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


# AVAX node configuration.
# Not to be confused with general Config at library root 

from avaxpython.utils.ip import DynamicIPDesc

# Config contains all of the configurations of an Avalanche node.
class Config:

    HTTP_PORT = 9650
    STAKING_PORT = 9651

    def __init__(self):

        self.EnableP2PTLS = True        
        self.TxFee=0
        # Transaction fee for transactions that create new state
        self.CreationTxFee=0
        # Staking uptime requirements
        self.UptimeRequirement=0.0
        # Minimum stake, in nAVAX, required to validate the primary network
        self.MinValidatorStake=0
        # Maximum stake, in nAVAX, allowed to be placed on a single validator in
        # the primary network
        self.MaxValidatorStake=0
        # Minimum stake, in nAVAX, that can be delegated on the primary network
        self.MinDelegatorStake=0
        # Minimum delegation fee, in the range [0, 1000000], that can be charged
        # for delegation on the primary network.
        self.MinDelegationFee=0
        # MinStakeDuration is the minimum amount of time a validator can validate
        # for in a single period.
        self.MinStakeDuration=60
        # MaxStakeDuration is the maximum amount of time a validator can validate
        # for in a single period.
        self.MaxStakeDuration=0
        # StakeMintingPeriod is the amount of time for a consumption period.
        self.StakeMintingPeriod=0
        # EpochFirstTransition is the time that the transition from epoch 0 to 1
        # should occur.
        self.EpochFirstTransition=0
        # EpochDuration is the amount of time that an epoch runs for.
        self.EpochDuration=0
        # Time that Apricot phase 0 rules go into effect
        self.ApricotPhase0Time=0

        # protocol to use for opening the network interface
        self.Nat = None # TODO nat.Router

        # Attempted NAT Traversal did we attempt
        self.AttemptedNATTraversal = False

        # ID of the network this node should connect to
        self.NetworkID = 0

        # Assertions configuration
        self.EnableAssertions = True

        # Crypto configuration
        self.EnableCrypto = True

        # Database to use for the node
        self.DB = None # TODO database.Database

        # Staking configuration
        # TODO obtain IP : port from configuration
        self.StakingIP : DynamicIPDesc = DynamicIPDesc("0.0.0.0", 9651)
        self.EnableP2PTLS = True # TODO          bool
        self.EnableStaking = True # TODO         bool
        self.StakingKeyFile = "" # TODO        string
        self.StakingCertFile = "" # TODO       string
        self.DisabledStakingWeight = 0 # TODO uint64

        # Throttling
        self.MaxNonStakerPendingMsgs=0 # TODO uint32
        self.StakerMSGPortion=0.0 # TODO        float64
        self.StakerCPUPortion=0.0 # TODO        float64
        self.SendQueueSize=0 # TODO           uint32
        self.MaxPendingMsgs=0 # TODO          uint32

        # Network configuration
        self.NetworkConfig = None # TODO timer.AdaptiveTimeoutConfig

        # Benchlist Configuration
        self.BenchlistConfig = None # TODO benchlist.Config

        # Bootstrapping configuration
        self.BootstrapPeers = [] # TODO []*Peer

        # HTTP configuration
        self.HTTPHost = "" # TODO string
        self.HTTPPort = 0 # TODO uint16

        self.HTTPSEnabled = True # TODO       bool
        self.HTTPSKeyFile = "" # TODO        string
        self.HTTPSCertFile = "" # TODO      string
        self.APIRequireAuthToken = True # bool
        self.APIAuthPassword = "" # TODO    string

        # Enable/Disable APIs
        self.AdminAPIEnabled = False # TODO    bool
        self.InfoAPIEnabled = False # TODO    bool
        self.KeystoreAPIEnabled = False # TODO bool
        self.MetricsAPIEnabled = False # TODO  bool
        self.HealthAPIEnabled = False # TODO  bool

        # Logging configuration
        self.LoggingConfig = None # TODO logging.Config

        # Plugin directory
        self.PluginDir = "" # TODO string

        # Consensus configuration
        self.ConsensusParams = None # TODO avalanche.Parameters

        # Throughput configuration
        self.ThroughputPort = 0 # TODO         uint16
        self.ThroughputServerEnabled = False # TODO bool

        # IPC configuration
        self.IPCAPIEnabled = False # TODO      bool
        self.IPCPath = "" # TODO            string
        self.IPCDefaultChainIDs = [] # TODO []string

        # Router that is used to handle incoming consensus messages
        self.ConsensusRouter = None # TODO         router.Router
        self.ConsensusGossipFrequency = 30 # TODO time.Duration
        self.ConsensusShutdownTimeout = 60 # TODO time.Duration

        # Dynamic Update duration for IP or NAT traversal
        self.DynamicUpdateDuration = 60 # TODO time.Duration

        self.DynamicPublicIPResolver = None # TODO dynamicip.Resolver

        # Throttling incoming connections
        self.ConnMeterResetDuration = 120 # TODO time.Duration
        self.ConnMeterMaxConns = 30 # TODO     int

        # Subnet Whitelist
        self.WhitelistedSubnets = {} # TODO ids.Set

        # Restart on disconnect settings
        self.RestartOnDisconnected = True # TODO     bool
        self.DisconnectedCheckFreq = 60 # TODO     time.Duration
        self.DisconnectedRestartTimeout = 60 # TODO time.Duration

        # Coreth
        self.CorethConfig = "" # TODO string

            