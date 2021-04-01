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


import re
from avaxpython import ids
from enum import Enum
from avaxpython.utils import nlimits

AvaxAssetIDBytesHex = "21e67317cbc4be2aeb00677ad6462778a8f52274b9d605df2591b23027a87dff"
assert len(AvaxAssetIDBytesHex) == 64

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

NullMsg = 0
GetAcceptedFrontierMsg = 1
AcceptedFrontierMsg = 2
GetAcceptedFrontierFailedMsg = 3
GetAcceptedMsg = 4
AcceptedMsg = 5
GetAcceptedFailedMsg = 6
GetMsg = 7
PutMsg = 8
GetFailedMsg = 9
PushQueryMsg = 10
PullQueryMsg = 11
ChitsMsg = 12
QueryFailedMsg = 13
ConnectedMsg = 14
DisconnectedMsg = 15
NotifyMsg = 16
GossipMsg = 17
GetAncestorsMsg = 18
MultiPutMsg = 19
GetAncestorsFailedMsg = 20


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