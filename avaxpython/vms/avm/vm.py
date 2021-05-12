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

from avaxpython.codec import linearcodec
from avaxpython.snow.engine.avalanche.vertex.vm import DAGVM
from avaxpython.snow.consensus.snowstorm.tx import Tx
from avaxpython.snow.choices.status import Status
from avaxpython.vms.avm.unique_tx import UniqueTx, TxState
from avaxpython.vms.avm.tx import Tx as AvmTx
from avaxpython.codec.manager import Manager as CodecManager
from avaxpython.codec.registry import Registry as CodecRegistry
from avaxpython.vms.avm.types import registered_types

batchTimeout       = 1
batchSize          = 30
stateCacheSize     = 30000
idCacheSize        = 30000
txCacheSize        = 30000
assetToFxCacheSize = 1024
maxUTXOsToFetch    = 1024
codecVersion = 0

errIncompatibleFx            = Exception("incompatible feature extension")
errUnknownFx                 = Exception("unknown feature extension")
errGenesisAssetMustHaveState = Exception("genesis asset must have non-empty state")
errWrongBlockchainID         = Exception("wrong blockchain ID")
errBootstrapping             = Exception("chain is currently bootstrapping")
errInsufficientFunds         = Exception("insufficient funds")



class VM(DAGVM):

    def __init__(self, codec = None, state = None, creationTxFee = None, txFee = None, genesisCodec: CodecManager = None, codecRegistry: CodecRegistry = None) -> None:
        self.codec = codec
        self.states = state
        self.genesisCodec: CodecManager = genesisCodec
        self.codecRegistry: CodecRegistry = codecRegistry

        if not self.codec:
            self.codec = CodecManager()


    def ParseTx(self, b: bytes) -> UniqueTx:
        """Parse bytes into a Tx"""

        rawTx = self.parsePrivateTx(b)
        
        if rawTx is None:
            return None

        tx = UniqueTx(
            TxState = TxState(
                Tx = rawTx,
            ),
            vm = self,
            txID = rawTx.ID(),
        )

        if not tx.SyntacticVerify():
            return None

        return tx
    
    def parsePrivateTx(self, txBytes: bytes) -> AvmTx:
        tx = AvmTx()
        self.codec.Unmarshal(txBytes, tx, type_ids = registered_types)
        unsigned_bytes = self.codec.Marshal(codecVersion, tx.UnsignedTx)
        
        tx.Initialize(unsigned_bytes, txBytes)
        return tx

