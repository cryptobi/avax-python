# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import re
from avaxpython import ids
from enum import Enum
from avaxpython.utils import nlimits

MainnetID = 1
CascadeID = 2
DenaliID  = 3
EverestID = 4
FujiID    = 5
TestnetID  = FujiID
UnitTestID = 10
LocalID    = 12345
MainnetName  = "mainnet"
CascadeName  = "cascade"
DenaliName   = "denali"
EverestName  = "everest"
FujiName     = "fuji"
TestnetName  = "testnet"
UnitTestName = "testing"
LocalName    = "local"
MainnetHRP  = "avax"
CascadeHRP  = "cascade"
DenaliHRP   = "denali"
EverestHRP  = "everest"
FujiHRP     = "fuji"
UnitTestHRP = "testing"
LocalHRP    = "local"
FallbackHRP = "custom"

PrimaryNetworkID = ids.Empty()
PlatformChainID  = ids.Empty()

NetworkIDToNetworkName = {
    MainnetID:  MainnetName,
    CascadeID:  CascadeName,
    DenaliID:   DenaliName,
    EverestID:  EverestName,
    FujiID:     FujiName,
    UnitTestID: UnitTestName,
    LocalID:    LocalName,
}

NetworkNameToNetworkID = {
    MainnetName:  MainnetID,
    CascadeName:  CascadeID,
    DenaliName:   DenaliID,
    EverestName:  EverestID,
    FujiName:     FujiID,
    TestnetName:  TestnetID,
    UnitTestName: UnitTestID,
    LocalName:    LocalID,
}

NetworkIDToHRP = {
    MainnetID:  MainnetHRP,
    CascadeID:  CascadeHRP,
    DenaliID:   DenaliHRP,
    EverestID:  EverestHRP,
    FujiID:     FujiHRP,
    UnitTestID: UnitTestHRP,
    LocalID:    LocalHRP,
}

NetworkHRPToNetwo = {
    MainnetHRP:  MainnetID,
    CascadeHRP:  CascadeID,
    DenaliHRP:   DenaliID,
    EverestHRP:  EverestID,
    FujiHRP:     FujiID,
    UnitTestHRP: UnitTestID,
    LocalHRP:    LocalID,
}

ValidNetworkName = re.compile(r'network-[0-9]+')

# NodeIDPrefix is used to denote node addresses rather than other addresses.
NodeIDPrefix = "NodeID-"

# SecretKeyPrefix is used to denote secret keys rather than other byte arrays.
SecretKeyPrefix = "PrivateKey-"

# Name of the platform
PlatformName = "avalanche"

# Name of the avalanche application
AppName = "avalanchego"

# DefaultHealthCheckExecutionPeriod is the default time between executions of a health check function
# Units in seconds
DefaultHealthCheckExecutionPeriod = 60
DefaultHealthCheckInitialDelay = 10

# MinConnectedStake is the minimum percentage of the Primary Network's that this node must be connected to to be considered healthy
MinConnectedStake = .80

# Request ID used when sending a Put message to gossip an accepted container (ie not sent in response to a Get)
GossipMsgRequestID = nlimits.limits(nlimits.c_uint32)[1]


# GetHRP returns the Human-Readable-Part of bech32 addresses for a networkID
def GetHRP(networkID):
    
    if networkID in NetworkIDToHRP:
        return NetworkIDToHRP[networkID]

    return FallbackHRP



# NetworkName returns a human readable name for the network with
# ID [networkID]
def NetworkName(networkID):
    if networkID in NetworkIDToNetworkName:
        return NetworkIDToNetworkName[networkID]

    return f"network-{networkID}"


# NetworkID returns the ID of the network with name [networkName]
def NetworkID(networkName):
    networkName = networkName.lower()
    if networkName in NetworkNameToNetworkID:
        return NetworkNameToNetworkID[networkName]

    id = int(networkName)
    if id > nlimits.limits(nlimits.c_uint32)[1]:
        raise Exception(f"networkID {networkName} not in [0, 2^32)")

    if ValidNetworkName.match(networkName):
        id = int(networkName[8:])
        if id > nlimits.limits(nlimits.c_uint32)[1]:
            raise Exception(f"networkID {networkName} not in [0, 2^32)")

        return id		

    raise Exception(f"failed to parse {networkName} as a network name")