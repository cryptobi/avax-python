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

# Node config. 
# This is specific to avalanchego. 
# Not to be confused with avaxpython.config() which is specific to the Python lib (logger, etc)

import os.path
from pathlib import Path
from avaxpython.utils import constants
from avaxpython.node.Config import Config as NodeConfig
from avaxpython.snow.networking.router.chain_router import ChainRouter
from avaxpython.main.keys import *
from avaxpython.utils.units.avax import *
from avaxpython.snow.networking.router.msg_manager import *

dbVersion = "v1.0.0"

Config = NodeConfig()

defaultNetworkName = constants.MainnetName
homeDir                = str(Path.home())
prefixedAppName        = f".{constants.AppName}"
defaultDataDir         = os.path.join(homeDir, prefixedAppName)
defaultDbDir           = os.path.join(defaultDataDir, "db")
defaultStakingKeyPath  = os.path.join(defaultDataDir, "staking", "staker.key")
defaultStakingCertPath = os.path.join(defaultDataDir, "staking", "staker.crt")
defaultPluginDirs      = [
    os.path.join(".", "build", "plugins"),
    os.path.join(".", "plugins"),
    os.path.join("/", "usr", "local", "lib", constants.AppName),
    os.path.join(defaultDataDir, "plugins"),
]

# GitCommit should be optionally set at compile time.
GitCommit = ""

# If true, print the version and quit.
versionKey = False # If true, print version and quit

# System
fdLimitKey = 1024 # Attempts to raise the process file descriptor limit to at least this value.

# Config
configFileKey = defaultString # Specifies a config file

# Genesis Config File
genesisConfigFileKey = "" # Specifies a genesis config file (ignored when running standard networks)

# Plugins
pluginDirKey = defaultString # Plugin directory for Avalanche VMs

# Network ID
networkNameKey = defaultNetworkName # Network ID this node will connect to

# AVAX fees
txFeeKey = MilliAvax # Transaction fee, in nAVAX
creationTxFeeKey = MilliAvax # Transaction fee, in nAVAX, for transactions that create new state
# Database
dbEnabledKey = True # Turn on persistent storage
dbPathKey = defaultDbDir, # Path to database directory

# Coreth Config
corethConfigKey = defaultString, # Specifies config to pass into coreth

# Logging
logsDirKey = "" # Logging directory for Avalanche
logLevelKey = "info", # The log level. Should be one of {verbo, debug, info, warn, error, fatal, off}
logDisplayLevelKey = "" # The log display level. If left blank, will inherit the value of log-level. Otherwise, should be one of {verbo, debug, info, warn, error, fatal, off}
logDisplayHighlightKey = "auto", # Whether to color/highlight display logs. Default highlights when the output is a terminal. Otherwise, should be one of {auto, plain, colors}

# Assertions
assertionsEnabledKey = True # Turn on assertion execution

# Signature Verification
signatureVerificationEnabledKey = True # Turn on signature verification

# Networking
# Public IP Resolution
publicIPKey = "" # Public IP of this node for P2P communication. If empty, try to discover with NAT. Ignored if dynamic-public-ip is non-empty.
dynamicUpdateDurationKey = 5 * 60, # Dynamic IP and NAT Traversal update duration
dynamicPublicIPResolverKey = "" # 'ifconfigco' (alias 'ifconfig') or 'opendns' or 'ifconfigme'. By default does not do dynamic public IP updates. If non-empty, ignores public-ip argument.

# Incoming Connection Throttling
# After we receive [conn-meter-max-conns] incoming connections from a given IP
# in the last [conn-meter-reset-duration], we close all subsequent incoming connections
# from the IP before upgrade.
connMeterResetDurationKey = 0

# Upgrade at most [conn-meter-max-conns] connections from a given IP per [conn-meter-reset-duration].
# If [conn-meter-reset-duration] is 0, incoming connections are not rate-limited.
# Upgrade at most [conn-meter-max-conns] connections from a given IP per [conn-meter-reset-duration]. 
# If [conn-meter-reset-duration] is 0, incoming connections are not rate-limited.
connMeterMaxConnsKey = 5

# Timeouts
networkInitialTimeoutKey = 5 # Initial timeout value of the adaptive timeout manager.
networkMinimumTimeoutKey = 2 # Minimum timeout value of the adaptive timeout manager.
networkMaximumTimeoutKey = 10 # Maximum timeout value of the adaptive timeout manager.
networkTimeoutHalflifeKey = 5 * 60 # Halflife of average network response time. Higher value --> network timeout is less volatile. Can't be 0.
networkTimeoutCoefficientKey = 2 # Multiplied by average network response time to get the network timeout. Must be >= 1.
sendQueueSizeKey = 4096 # Max number of messages waiting to be sent to peers.

# Restart on Disconnect
disconnectedCheckFreqKey = 10 # How often the node checks if it is connected to any peers.

# See [restart-on-disconnected]. If 0, node will not restart due to disconnection.
disconnectedRestartTimeoutKey = 1 * 60 # If [restart-on-disconnected], node restarts if not connected to any peers for this amount of time. 

# If 0, node will not restart due to disconnection.
restartOnDisconnectedKey = False # If true, this node will restart if it is not connected to any peers for [disconnected-restart-timeout].

# Peer alias configuration
# How often the node will attempt to connect 
# to an IP address previously associated with a peer (i.e. a peer alias).
peerAliasTimeoutKey = 10 * 60

# Benchlist
benchlistFailThresholdKey = 10 # Number of consecutive failed queries before benchlisting a node.
benchlistPeerSummaryEnabledKey = False # Enables peer specific query latency metrics.
benchlistDurationKey = 30*60 # Max amount of time a peer is benchlisted after surpassing the threshold.
benchlistMinFailingDurationKey = 5*60 # Minimum amount of time messages to a peer must be failing before the peer is benched.

# Router
maxNonStakerPendingMsgsKey = int(DefaultMaxNonStakerPendingMsgs) # Maximum number of messages a non-staker is allowed to have pending.
stakerMsgReservedKey = DefaultStakerPortion # Reserve a portion of the chain message queue's space for stakers.
stakerCPUReservedKey = DefaultStakerPortion # Reserve a portion of the chain's CPU time for stakers.
maxPendingMsgsKey = 4096 # Maximum number of pending messages. Messages after this will be dropped.
consensusGossipFrequencyKey = 10 # Frequency of gossiping accepted frontiers.
consensusShutdownTimeoutKey = 5 # Timeout before killing an unresponsive chain.

# HTTP API
httpHostKey = "127.0.0.1" # Address of the HTTP server
httpPortKey = 9650 # Port of the HTTP server
httpsEnabledKey = False # Upgrade the HTTP server to HTTPs
httpsKeyFileKey = "" # TLS private key file for the HTTPs server
httpsCertFileKey = "" # TLS certificate file for the HTTPs server
httpAllowedOrigins = "*" # Origins to allow on the HTTP port. Defaults to * which allows all origins. Example: https://*.avax.network https://*.avax-test.network
apiAuthRequiredKey = False # Require authorization token to call HTTP APIs
apiAuthPasswordFileKey = "" # Password file used to initially create/validate API authorization tokens. Leading and trailing whitespace is removed from the password. Can be changed via API call.

# Enable/Disable APIs
adminAPIEnabledKey = False # If true, this node exposes the Admin API
infoAPIEnabledKey = True # If true, this node exposes the Info API
keystoreAPIEnabledKey = True # If true, this node exposes the Keystore API
metricsAPIEnabledKey = True # If true, this node exposes the Metrics API
healthAPIEnabledKey = True # If true, this node exposes the Health API
ipcAPIEnabledKey = False # If true, IPCs can be opened

# Throughput Server (deprecated)
xputServerPortKey = 9652 # Port of the deprecated throughput test server
xputServerEnabledKey = False # If true, throughput test server is created

# Health
healthCheckFreqKey = 30 # Time between health checks
healthCheckAveragerHalflifeKey = 10 # Halflife of averager when calculating a running average in a health check

# Network Layer Health
networkHealthMaxTimeSinceMsgSentKey = 60 # Network layer returns unhealthy if haven't sent a message for at least this much time
networkHealthMaxTimeSinceMsgReceivedKey = 60 # Network layer returns unhealthy if haven't received a message for at least this much time
networkHealthMaxPortionSendQueueFillKey = 0.9 # Network layer returns unhealthy if more than this portion of the pending send queue is full
networkHealthMinPeersKey = 1 # Network layer returns unhealthy if connected to less than this many peers
networkHealthMaxSendFailRateKey = .9 # Network layer reports unhealthy if more than this portion of attempted message sends fail

# Router Health
routerHealthMaxDropRateKey = 1 # Node reports unhealthy if the router drops more than this portion of messages.
routerHealthMaxOutstandingRequestsKey = 1024 # Node reports unhealthy if there are more than this many outstanding consensus requests (Get, PullQuery, etc.) over all chains
networkHealthMaxOutstandingDurationKey = 5*60 # Node reports unhealthy if there has been a request outstanding for this duration

# Staking
stakingPortKey = 9651 # Port of the consensus server
stakingEnabledKey = True # Enable staking. If enabled, Network TLS is required.
p2pTLSEnabledKey = True # Require TLS to authenticate network communication
stakingKeyPathKey = defaultString # Path to the TLS private key for staking
stakingCertPathKey = defaultString # Path to the TLS certificate for staking
stakingDisabledWeightKey = 1 # Weight to provide to each peer when staking is disabled

# Uptime Requirement
uptimeRequirementKey = .6 # Fraction of time a validator must be online to receive rewards

# Minimum Stake required to validate the Primary Network
minValidatorStakeKey = 2 * KiloAvax # Minimum stake, in nAVAX, required to validate the primary network

# Maximum Stake that can be staked and delegated to a validator on the Primary Network
maxValidatorStakeKey = 3 * MegaAvax # Maximum stake, in nAVAX, that can be placed on a validator on the primary network

# Minimum Stake that can be delegated on the Primary Network
minDelegatorStakeKey = 25 * Avax # Minimum stake, in nAVAX, that can be delegated on the primary network
minDelegatorFeeKey = 20000 # Minimum delegation fee, in the range [0, 1000000], that can be charged for delegation on the primary network

# Minimum Stake Duration
minStakeDurationKey = 24*(60*60) # Minimum staking duration

# Maximum Stake Duration
maxStakeDurationKey = 365*24*(60*60) # Maximum staking duration

# Stake Minting Period
stakeMintingPeriodKey = 365*24*(60*60) # Consumption period of the staking function

# Subnets
whitelistedSubnetsKey = "" # Whitelist of subnets to validate.

# Bootstrapping
bootstrapIPsKey, defaultString, # Comma separated list of bootstrap peer ips to connect to. Example: 127.0.0.1:9630,127.0.0.1:9631
bootstrapIDsKey, defaultString, # Comma separated list of bootstrap peer ids to connect to. Example: NodeID-JR4dVmy6ffUGAKCBDkyCbeZbyHQBeDsET,NodeID-8CrVPQZ4VSqgL8zTdvL14G8HqAfrBr4z
retryBootstrap = True # Specifies whether bootstrap should be retried
retryBootstrapMaxAttempts, 50, # Specifies how many times bootstrap should be retried

# Consensus
snowSampleSizeKey = 20 # Number of nodes to query for each network poll
snowQuorumSizeKey = 14 # Alpha value to use for required number positive results
snowVirtuousCommitThresholdKey = 15, # Beta value to use for virtuous transactions
snowRogueCommitThresholdKey = 20 # Beta value to use for rogue transactions
snowAvalancheNumParentsKey = 5 # Number of vertexes for reference from each new vertex
snowAvalancheBatchSizeKey = 30 # Number of operations to batch in each new vertex
snowConcurrentRepollsKey = 4 # Minimum number of concurrent polls for finalizing consensus
snowOptimalProcessingKey = 50 # Optimal number of processing vertices in consensus
snowMaxProcessingKey = 1024 # Maximum number of processing items to be considered healthy
snowMaxTimeProcessingKey = 2*60 # Maximum amount of time an item should be processing and still be healthy
snowEpochFirstTransition = 1607626800 # Unix timestamp of the first epoch transaction, in seconds. Defaults to 12/10/2020 @ 7:00pm (UTC)
snowEpochDuration = 6 * (60*60) # Duration of each epoch

# IPC
ipcsChainIDsKey = "" # Comma separated list of chain ids to add to the IPC engine. Example: 11111111111111111111111111111111LpoYY,4R5p2RXDGLqaifZE4hHWH9owe34pfoBULn1DrQTWivjg8o4aH
ipcsPathKey = defaultString # The directory (Unix) or named pipe name prefix (Windows) for IPC sockets


def setNodeConfig():
    """Go interface preserved as much as possible."""
    global Config

    Config.ConsensusParams.K = snowSampleSizeKey
    Config.ConsensusParams.Alpha = snowQuorumSizeKey
    Config.ConsensusParams.BetaVirtuous = snowVirtuousCommitThresholdKey
    Config.ConsensusParams.BetaRogue = snowRogueCommitThresholdKey
    Config.ConsensusParams.Parents = snowAvalancheNumParentsKey
    Config.ConsensusParams.BatchSize = snowAvalancheBatchSizeKey
    Config.ConsensusParams.ConcurrentRepolls = snowConcurrentRepollsKey
    Config.ConsensusParams.OptimalProcessing = snowOptimalProcessingKey
    Config.ConsensusParams.MaxOutstandingItems = snowMaxProcessingKey
    Config.ConsensusParams.MaxItemProcessingTime = snowMaxTimeProcessingKey

    Config.ConsensusRouter = ChainRouter()


def parseCmdLine():
    """Parse command line args into the main Config object. 
    Analog to parseViper on the Go implementation.
    Go interface preserved as much as possible."""
    return setNodeConfig()
