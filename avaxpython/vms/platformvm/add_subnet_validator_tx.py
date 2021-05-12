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

from avaxpython.vms.platformvm.base_tx import BaseTx
from avaxpython.vms.components.verify.verification import Verifiable
from avaxpython.vms.platformvm.validator import Validator, SubnetValidator
from avaxpython.structured import AvaxStructured

errDSValidatorSubset = Exception("all subnets' staking period must be a subset of the primary network")

class UnsignedAddSubnetValidatorTx(AvaxStructured):
    """UnsignedAddSubnetValidatorTx is an unsigned addSubnetValidatorTx"""

    _avax_tags = [
        ("BaseTx", { "serialize": True}),
        ("Validator", { "serialize": True, "json": "validator"}),
        ("SubnetAuth", { "serialize": True, "json": "subnetAuthorization"}),
    ]

    def __init__(self) -> None:
        
        # Metadata, inputs and outputs
        self.BaseTx = BaseTx()
        # The validator
        self.Validator = SubnetValidator() 
        # Auth that will be allowing this validator into the network
        self.SubnetAuth = Verifiable()


    def StartTime(self):
        """StartTime of this validator"""
        return self.Validator.StartTime()

    # EndTime of this validator
    def EndTime(self):
        return self.Validator.EndTime()

    # Weight of this validator
    def Weight(self):
        return self.Validator.Weight()
    
    def Verify(ctx, c, feeAmount, feeAssetID, minStakeDuration, maxStakeDuration):
        """Verify return None iff [tx] is valid"""        
    
    def SemanticVerify(vm, db, stx):
        """SemanticVerify this transaction is valid."""
    
    def InitiallyPrefersCommit(vm):
        """InitiallyPrefersCommit returns true if the proposed validators start time is after the current wall clock time,"""
        
    

