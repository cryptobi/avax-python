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

from avaxpython.vms.components.avax.transferables import TransferableInput
from avaxpython.vms.avm.base_tx import BaseTx
from avaxpython.ids.ID import ID
from avaxpython.types import Slice
from avaxpython.structured import AvaxStructured

errNoImportInputs = Exception("no import inputs")

class ImportTx(AvaxStructured):
    """ImportTx is a transaction that imports an asset from another blockchain."""
    _avax_tags = [
        ("BaseTx", { "serialize": True}),
        ("SourceChain", { "serialize": True, "json" : "sourceChain" }),
        ("ImportedIns", { "element_type": TransferableInput, "serialize": True, "json":"importedInputs"}),
    ]

    def __init__(self) -> None:
        
        self.BaseTx = BaseTx()

        # Which chain to consume the funds from
        self.SourceChain = ID()

        # The inputs to this transaction
        self.ImportedIns = Slice()
    
    def InputUTXOs(self):
        """InputUTXOs track which UTXOs this transaction is consuming."""
        utxos = self.BaseTx.InputUTXOs()
        for inx in self.ImportedIns:
            inx.Symbol = True
            utxos.append(inx.UTXOID)
        
        return utxos
        
    def ConsumedAssetIDs(self):
        """ConsumedAssetIDs returns the IDs of the assets this transaction consumes"""
        assets = self.BaseTx.AssetIDs()
        for inx in self.ImportedIns:
            assets.Add(inx.AssetID())
        
        return assets
        
    def AssetIDs(self):
        """AssetIDs returns the IDs of the assets this transaction depends on"""
        assets = self.BaseTx.AssetIDs()
        for inx in self.ImportedIns:
            assets.Add(inx.AssetID())
        
        return assets
        
    def NumCredentials(self):
        """NumCredentials returns the number of expected credentials"""
        return self.BaseTx.NumCredentials() + len(self.ImportedIns)

    def SyntacticVerify(self, ctx, c, txFeeAssetID, txFee, a, numFxs):
        """SyntacticVerify that this transaction is well-formed."""
    
    def SemanticVerify(selfvm, tx, creds):
        """SemanticVerify that this transaction is well-formed."""
    
    def ExecuteWithSideEffects(selfvm, batch):
        """ExecuteWithSideEffects writes the batch with any additional side effects"""

    def __struct__(self):
        _d = {}
        for k, v in self._avax_tags:
            if "__struct__" in dir():
                _d[k] = getattr(self, k).__struct__()
            else:
                _d[k] = getattr(self, k)
        return str(_d)


    def __repr__(self):
        return str(self.__struct__())