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
from avaxpython import ids

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
NetworkHRPToNetworkID = {
    MainnetHRP:  MainnetID,
    CascadeHRP:  CascadeID,
    DenaliHRP:   DenaliID,
    EverestHRP:  EverestID,
    FujiHRP:     FujiID,
    UnitTestHRP: UnitTestID,
    LocalHRP:    LocalID,
}

ValidNetworkPrefix = "network-"

def GetHRP(networkID: int) -> str:
    """GetHRP returns the Human-Readable-Part of bech32 addresses for a networkID"""
    if networkID in NetworkIDToHRP:
        return NetworkIDToHRP[networkID]

    return FallbackHRP


def NetworkName(networkID: int) -> str:
    """NetworkName returns a human readable name for the network with ID [networkID]"""

    if networkID in NetworkIDToNetworkName:
        return NetworkIDToNetworkName[networkID]

    return f"network-{networkID}"


def NetworkID(networkName: str) -> int:
    """NetworkID returns the ID of the network with name [networkName]"""
    networkName = networkName.lower()
    if networkName in NetworkNameToNetworkID:
        return NetworkNameToNetworkID[networkName]

    idStr = networkName
    if networkName.startswith(ValidNetworkPrefix):
        idStr = networkName[len(ValidNetworkPrefix):]
    
    return int(idStr)
    