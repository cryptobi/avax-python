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

from avaxpython.vms.avm.base_tx import BaseTx
from avaxpython.vms.avm.operation import Operation
from avaxpython.structured import AvaxStructured

errOperationsNotSortedUnique = Exception("operations not sorted and unique")
errNoOperations              = Exception("an operationTx must have at least one operation")
errDoubleSpend               = Exception("inputs attempt to double spend an input")


class OperationTx(AvaxStructured):
    """OperationTx is a transaction with no credentials."""
    _avax_tags = [
        ("BaseTx", { "serialize": True}),
        ("Ops", { "element_type": Operation, "serialize": True, "json":"operations"}),
    ]

    def __init__(self) -> None:        
        self.BaseTx = BaseTx()
        self.Ops = Slice()
    
    def Operations(self):
        """Operations track which ops this transaction is performing. The returned array should not be modified."""
        return self.Ops
    
    def InputUTXOs(self):
        """InputUTXOs track which UTXOs this transaction is consuming."""
        utxos = self.BaseTx.InputUTXOs()
        for op in self.Ops:
            utxos = append(utxos, op.UTXOIDs)
        
        return utxos
        
    def ConsumedAssetIDs(self):
        """ConsumedAssetIDs returns the IDs of the assets this transaction consumes"""
        assets = self.BaseTx.AssetIDs()
        for op in self.Ops:
            if len(op.UTXOIDs) > 0:
                assets.Add(op.AssetID())        
        
        return assets
    
    def AssetIDs(self):
        """AssetIDs returns the IDs of the assets this transaction depends on"""
        assets = self.BaseTx.AssetIDs()
        for op in self.Op:
            assets.Add(op.AssetID())    
        return assets
        
    def NumCredentials(self) -> int:
        """NumCredentials returns the number of expected credentials"""
        return self.BaseTx.NumCredentials() + len(self.Ops)
    
    def UTXOs(self):
        """UTXOs returns the UTXOs transaction is producing."""
        txID = self.ID()
        utxos = self.BaseTx.UTXOs()

        for op in self.Ops:
            asset = op.AssetID()
            for out in op.Op.Outs():
                utxos.append(avax.UTXO(
                    UTXOID = avax.UTXOID(
                        TxID=        txID,
                        OutputIndex = len(xos),
                    ),
                    Asset = avax.Asset(ID = asset),
                    Out =  out,
                ))

        return utxos
    
    def SyntacticVerify(ctx, c, txFeeAssetID, txFee, a, numFxs):
        """SyntacticVerify that this transaction is well-formed."""

    
    def SemanticVerify(vm, tx, creds):
        """SemanticVerify that this transaction is well-formed."""
