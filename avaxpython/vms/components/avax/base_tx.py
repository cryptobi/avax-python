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
from avaxpython.types import *
from avaxpython.ids.ID import ID
from avaxpython.vms.components.avax.metadata import Metadata
from avaxpython.vms.components.avax.transferables import TransferableOutput, TransferableInput
from avaxpython.vms.components.avax.utxo_id import UTXOID
from avaxpython.vms.components.avax.utxo import UTXO
from avaxpython.vms.components.avax.asset import Asset
from avaxpython.structured import AvaxStructured

# MaxMemoSize is the maximum number of bytes in the memo field
MaxMemoSize = 256

errNilTx          = Exception("nil tx is not valid")
errWrongNetworkID = Exception("tx has wrong network ID")
errWrongChainID   = Exception("tx has wrong chain ID")


class BaseTx(Metadata, AvaxStructured): 	
    """BaseTx is the basis of all standard transactions."""

    _avax_tags = [
        ("NetworkID", {"serialize": True, "json": "networkID" }),
        ("BlockchainID", {"serialize": True, "json" : "blockchainID" }),
        ("Outs", {"element_type": TransferableOutput, "serialize": True, "json":"outputs"}),
        ("Ins", {"element_type": TransferableInput, "serialize": True, "json":"inputs"}),
        ("Memo", {"element_type": Byte, "serialize": True, "json":"memo"}),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.NetworkID = Uint32()
        self.BlockchainID = ID()
        self.Outs = Slice()
        self.Ins = Slice()
        self.Memo = Slice()


    # InputUTXOs track which UTXOs this transaction is consuming.
    def InputUTXOs(self) -> List[UTXOID]:
        utxos = []
        i = 0
        for inx in self.Ins:
            utxos[i] = inx.UTXOID
            i += 1
        
        return utxos
    
    
    def ConsumedAssetIDs(self):
        """ConsumedAssetIDs returns the IDs of the assets this transaction consumes"""
        assets = set()
        for inx in self.Ins:
            assets.Add(inx.AssetID())

        return assets
    
    def AssetIDs(self): 
        """AssetIDs returns the IDs of the assets this transaction depends on"""
        return self.ConsumedAssetIDs()
    
    def NumCredentials(self):
        return len(self.Ins)

    # UTXOs returns the UTXOs transaction is producing.
    def UTXOs(self):
        txID = self.ID()
        utxos = []
        i = 0
        for out in self.Outs:
            utxo = UTXO(
                UTXOID = UTXOID(
                    TxID=txID,
                    OutputIndex = Uint32(i),
                ),
                Asset = Asset(ID = out.AssetID()),
                Out = out.Out,
            )
            utxos.append(utxo) 
            i += 1
    

    # MetadataVerify ensures that transaction metadata is valid
    def MetadataVerify(self, ctx):
        if self.NetworkID != ctx.NetworkID:
            raise errWrongNetworkID
        elif self.BlockchainID != ctx.ChainID:
            raise errWrongChainID
        elif len(self.Memo) > MaxMemoSize:
            raise Exception(f"memo length, {len(self.Memo)}, exceeds maximum memo length, {MaxMemoSize}")
        else:
            return self.Metadata.Verify()

