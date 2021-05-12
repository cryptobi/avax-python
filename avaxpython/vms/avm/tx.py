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
from avaxpython.vms.components.verify.verification import Verifiable
from avaxpython.ids.ID import ID as LongID
from avaxpython.vms.components.avax.utxo import UTXO
from avaxpython.vms.components.avax.utxo_id import UTXOID
from avaxpython.snow.context import Context
from avaxpython.types import *
from avaxpython.structured import AvaxStructured
from avaxpython.utils.hashing import hashing

class UnsignedTx:

    _avax_interface = True

    def __init__(self) -> None:
        self.Bytes: bytes = None

    def Initialize(self, unsignedBytes: bytes, bbytes: bytes):
        self.Bytes = bbytes
        self.unsignedBytes = unsignedBytes

    def ID(self) -> LongID:
        pass

    def UnsignedBytes(self) -> bytes:
        return self.unsignedBytes

    def Bytes(self) -> bytes:
        pass

    def ConsumedAssetIDs(self):
        pass

    def AssetIDs(self):
        pass

    def NumCredentials(self):
        pass

    def InputUTXOs(self) -> List[UTXOID]:
        pass

    def UTXOs(self) -> List[UTXO]:
        pass

    def SyntacticVerify(ctx, c, txFeeAssetID, txFee, creationTxFee, numFxs):
        pass

    def SemanticVerify(vm, tx, creds):
        pass

    def ExecuteWithSideEffects(vm, batch):
        pass

    def __struct__(self):
        _s = {
            'UnsignedTx' : 'Unsigned Tx Interface'
        }
        return _s

class Tx(AvaxStructured):

    _avax_tags = [
        ("UnsignedTx", { "serializeV0": True, "serialize": True, "json" : "unsignedTx" }),
        ("Creds", { "element_type": Verifiable, "serializeV0": True, "serialize": True, "json":"credentials"}),
    ]

    def __init__(self):        
        # The credentials of this transaction
        self.UnsignedTx = UnsignedTx()
        self.Creds: List[Verifiable] = Slice()

    def Initialize(self, unsignedBytes, bbytes: bytes):
        self.id = hashing.ComputeHash256Array(bbytes)
        self.unsignedBytes = unsignedBytes
        self.bytes = bbytes

    def ID(self):
        return self.id