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

from avaxpython.vms.platformvm.validator import Validator
from avaxpython.vms.platformvm.base_tx import BaseTx
from avaxpython.vms.components.avax.transferables import TransferableOutput
from avaxpython.vms.components.verify.verification import Verifiable
from avaxpython.structured import AvaxStructured
from avaxpython.types import Slice

errDelegatorSubset = Exception("delegator's time range must be a subset of the validator's time range")
errInvalidState    = Exception("generated output isn't valid state")
errCapWeightBroken = Exception("validator would surpass maximum weight")
errOverDelegated   = Exception("validator would be over delegated")

class UnsignedAddDelegatorTx(AvaxStructured):
    """UnsignedAddDelegatorTx is an unsigned addDelegatorTx"""

    _avax_tags = [
        ("BaseTx", { "serialize": True}),
        ("Validator", { "serialize": True, "json": "validator"}),
        ("Stake", { "element_type": TransferableOutput, "serialize": True, "json": "stake"}),
        ("RewardsOwner", { "serialize": True, "json": "rewardsOwner"}),
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
    
    def StartTime(self):
        """StartTime of this validator"""
        return self.Validator.StartTime()
        
    def EndTime(self):
        """EndTime of this validator"""
        return self.Validator.EndTime()
        
    def Weight(self):
        """Weight of this validator"""
        return self.Validator.Weight()    
    
    def Verify(self, ctx, c, minDelegatorStake, minStakeDuration, maxStakeDuration):
        """Verify return None iff [tx] is valid"""        
    
    def SemanticVerify(self, vm, db, stx):
        """SemanticVerify this transaction is valid."""
    
    def InitiallyPrefersCommit(self, vm):
        """InitiallyPrefersCommit returns true if the proposed validators start time is after the current wall clock time"""
        return self.StartTime().After(vm.clock.Time())

