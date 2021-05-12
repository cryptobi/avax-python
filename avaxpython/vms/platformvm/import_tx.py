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

from avaxpython.types import Slice
from avaxpython.ids.ID import ID
from avaxpython.vms.platformvm.base_tx import BaseTx
from avaxpython.vms.components.avax.transferables import TransferableInput
from avaxpython.structured import AvaxStructured

errAssetIDMismatch          = Exception("asset IDs in the input don't match the utxo")
errWrongNumberOfCredentials = Exception("should have the same number of credentials as inputs")
errNoImportInputs           = Exception("tx has no imported inputs")
errInputsNotSortedUnique    = Exception("inputs not sorted and unique")

class UnsignedImportTx(AvaxStructured):
    """UnsignedImportTx is an unsigned ImportTx"""

    _avax_tags = [
        ("BaseTx", { "serialize": True}),
        ("SourceChain", { "serialize": True, "json": "sourceChain"}),
        ("ImportedInputs", {  "element_type": TransferableInput, "serialize": True, "json": "importedInputs"}),
    ]

    def __init__(self) -> None:
        
        self.BaseTx = BaseTx()

        # Which chain to consume the funds from
        self.SourceChain = ID()

        # Inputs that consume UTXOs produced on the chain
        self.ImportedInputs = Slice()
    
    def InputUTXOs(self):
        """InputUTXOs returns the UTXOIDs of the imported funds"""
        setx = {}
        for inx in self.ImportedInputs:
            setx.add(inx.InputID())
        
        return setx

    def  Verify(self, avmID, ctx, c, feeAmount, feeAssetID):
        """Verify this transaction is well-formed"""

    def  SemanticVerify(self, vm, db, stx):
        """SemanticVerify this transaction is valid."""

    def Accept(self, ctx, batch):
        """Accept this transaction and spend imported inputs
        We spend imported UTXOs here rather than in semanticVerify because
        we don't want to remove an imported UTXO in semanticVerify
        only to have the transaction not be Accepted. This would be inconsistent.
        Recall that imported UTXOs are not kept in a versionDB."""
        utxoIDs = []
        for inx in self.ImportedInputs:
            utxoID = inx.InputID()
            utxoIDs.append(utxoID[:])		

