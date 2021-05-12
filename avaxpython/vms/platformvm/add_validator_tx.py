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

from avaxpython.types import *
from avaxpython.vms.components.avax.transferables import TransferableOutput
from avaxpython.vms.platformvm.base_tx import BaseTx
from avaxpython.vms.platformvm.validator import Validator
from avaxpython.vms.components.verify.verification import Verifiable
from avaxpython.vms.platformvm.vm_constants import PercentDenominator
from avaxpython.structured import AvaxStructured

errNilTx                     = Exception("tx is nil")
errWeightTooSmall            = Exception("weight of this validator is too low")
errWeightTooLarge            = Exception("weight of this validator is too large")
errStakeTooShort             = Exception("staking period is too short")
errStakeTooLong              = Exception("staking period is too long")
errInsufficientDelegationFee = Exception("staker charges an insufficient delegation fee")
errTooManyShares             = Exception(f"a staker can only require at most {PercentDenominator} shares from delegators")

class UnsignedAddValidatorTx(AvaxStructured):
    """UnsignedAddValidatorTx is an unsigned addValidatorTx"""
    _avax_tags = [
        ("BaseTx", { "serialize": True}),
        ("Validator", { "serialize": True, "json": "validator"}),
        ("Stake", { "element_type": TransferableOutput, "serialize": True, "json": "stake"}),
        ("RewardsOwner", { "serialize": True, "json": "rewardsOwner"}),
        ("Shares", { "serialize": True, "json": "shares"}),
    ]

    def __init__(self) -> None:
        
        # Metadata, inputs and outputs
        self.BaseTx = BaseTx()
        # Describes the delegatee
        self.Validator = Validator()
        # Where to send staked tokens when done validating
        self.Stake = Slice()
        # Where to send staking rewards when done validating
        self.RewardsOwner = Verifiable()
        # Fee this validator charges delegators as a percentage, times 10,000
        # For example, if this validator has Shares=300,000 then they take 30% of rewards from delegators
        self.Shares = Uint32()

    # StartTime of this validator
    def StartTime(self):
        return self.Validator.StartTime()

    # EndTime of this validator
    def EndTime(self):
        return self.Validator.EndTime()

    # Weight of this validator
    def Weight(self):
        return self.Validator.Weight()
