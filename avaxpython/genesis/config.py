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

from typing import List
from avaxpython.ids.ShortID import ShortID

class LockedAmount:

    def __init__(self):
        self.Amount: int
        self.Locktime: int


class Allocation:
    def __init__(self):
        self.ETHAddr: ShortID
        self.AVAXAddr: ShortID
        self.InitialAmount: int
        self.UnlockSchedule: List[LockedAmount]


class UnparsedAllocation:

    def __init__(self):
        self.ETHAddr: str
        self.AVAXAddr: str
        self.InitialAmount: int
        self.UnlockSchedule: List[LockedAmount]


class UnparsedStaker:
    def __init__(self):        
        self.NodeID: str
        self.RewardAddress: str
        self.DelegationFee: int




class Staker:
    def __init__(self):    
        self.NodeID: ShortID
        self.RewardAddress: ShortID
        self.DelegationFee: int


    def Unparse(self, networkID: int) -> UnparsedStaker:
        avaxAddr = formatting.FormatAddress("X", constants.GetHRP(networkID), s.RewardAddress.Bytes())
        return UnparsedStaker(
            NodeID=self.NodeID.PrefixedString(constants.NodeIDPrefix),
            RewardAddress=avaxAddr,
            DelegationFee=self.DelegationFee,
        )



class Config:

    def __init__(self):
        self.NetworkID: int
        self.Allocations: List[Allocation]
        self.StartTime: int
        self.InitialStakeDuration: int
        self.InitialStakeDurationOffset: int
        self.InitialStakedFunds: List[ShortID]
        self.InitialStakers: List[Staker]
        self.CChainGenesis: str
        self.Message:str


def GetConfig(networkID: int) -> Config:
	
    if networkID == constants.MainnetID:
        return MainnetConfig
    elif networkID == constants.FujiID:
        return FujiConfig
    elif networkID == constants.LocalID:
        return LocalConfig
    else:
        tempConfig = LocalConfig
        tempConfig.NetworkID = networkID
        return tempConfig
