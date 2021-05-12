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
from avaxpython.structured import AvaxStructured
from avaxpython.vms.platformvm.base_tx import BaseTx
from avaxpython.types import Bytes, Slice
from avaxpython.vms.components.verify.verification import Verifiable

errInvalidVMID             = Exception("invalid VM ID")
errFxIDsNotSortedAndUnique = Exception("feature extensions IDs must be sorted and unique")
errNameTooLong             = Exception("name too long")
errGenesisTooLong          = Exception("genesis too long")
errIllegalNameCharacter    = Exception("illegal name character")
maxNameLen    = 1 << 7
maxGenesisLen = 1 << 20

class UnsignedCreateChainTx(AvaxStructured):
    """UnsignedCreateChainTx is an unsigned CreateChainTx"""
    _avax_tags = [
        ("BaseTx", { "serialize": True}),
        ("SubnetID", { "serialize": True, "json": "subnetID"}),
        ("ChainName", {  "serialize": True, "json": "chainName"}),
        ("VMID", { "serialize": True, "json": "vmID"}),
        ("FxIDs", { "element_type": ID, "serialize": True, "json": "fxIDs"}),
        ("GenesisData", { "serialize": True, "json": "genesisData"}),
        ("SubnetAuth", { "serialize": True, "json": "subnetAuthorization"}),
    ]

    def __init__(self) -> None:
        
        # Metadata, inputs and outputs
        self.BaseTx = BaseTx()
        # ID of the Subnet that validates this blockchain
        self.SubnetID = ID()
        # A human readable name for the chain; need not be unique
        self.ChainName = str()
        # ID of the VM running on the new chain
        self.VMID = ID()
        # IDs of the feature extensions running on the new chain
        self.FxIDs = Slice()
        # Byte representation of genesis state of the new chain
        self.GenesisData = Bytes()
        # Auth that will be allowing this validator into the network
        self.SubnetAuth = Verifiable()

    def Verify(self, ctx, c, feeAmount, feeAssetID):
        """Verify this transaction is well-formed"""

    def SemanticVerify(self, vm, db, stx):
        """SemanticVerify this transaction is valid."""

