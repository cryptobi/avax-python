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
from avaxpython.utils import hashing
from avaxpython.types import *
from avaxpython.vms.platformvm.codec import codecVersion
from avaxpython.vms.secp256k1fx.credential import Credential
from avaxpython.vms.components.verify.verification import Verifiable
from avaxpython.structured import AvaxStructured

class UnsignedTx:
    """UnsignedTx is an unsigned transaction"""
    _avax_interface = True
    def Initialize(self, unsignedBytes, signedBytes: bytes):
        pass

    def ID(self) -> ID:
        pass

    def UnsignedBytes(self) -> bytes:
        pass

    def Bytes(self) -> bytes:
        pass


class UnsignedDecisionTx(UnsignedTx):
    """UnsignedDecisionTx is an unsigned operation that can be immediately decided"""	

    _avax_interface = True

    def SemanticVerify(self, vm, db, stx):
        """Attempts to verify this transaction with the provided state."""		
        pass



class UnsignedProposalTx(UnsignedTx):
    """UnsignedProposalTx is an unsigned operation that can be proposed"""

    _avax_interface = True

    def SemanticVerify(self, vm, db, stx):
        """Check Tx semantics"""
        pass



# UnsignedAtomicTx is an unsigned operation that can be atomically accepted
class UnsignedAtomicTx(UnsignedTx):

    _avax_interface = True

    def InputUTXOs(self):
        """UTXOs this tx consumes"""
        pass
	
    def SemanticVerify(self, vm, db, stx):
        """Attempts to verify this transaction with the provided state."""
        pass
    
    def Accept(self, ctx, batch):
        """Accept this transaction with the additionally provided state transitions."""
        pass



class Tx(AvaxStructured):
    """Tx is a signed transaction"""	

    _avax_tags = [
        ("UnsignedTx", { "serialize": True,  "json": "unsignedTx"}),
        ("Creds", { "element_type": Verifiable, "serialize": True, "json":"credentials"}),
    ]		

    def __init__(self) -> None:
        self.UnsignedTx = UnsignedTx()
        self.Creds = Slice()

