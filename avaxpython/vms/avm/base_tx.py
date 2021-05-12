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

from avaxpython.vms.components.avax.base_tx import BaseTx as AvaxBaseTx
from avaxpython.structured import AvaxStructured

errNilTx = Exception("nil tx is not valid")

class BaseTx(AvaxStructured):
    """BaseTx is the basis of all transactions."""
    _avax_tags = [
        ("BaseTx", {"serialize": True, "json": "" }), 
    ]

    def __init__(self) -> None:
	    self.BaseTx  = AvaxBaseTx()
        

def SyntacticVerify(self, ctx, c, txFeeAssetID, txFee, a, b):
    """SyntacticVerify that this transaction is well-formed."""
    return None

def SemanticVerify(self, vm, tx, creds):
    """SemanticVerify that this transaction is valid to be spent."""
    return None

def ExecuteWithSideEffects(self, vm, batch):
    """ExecuteWithSideEffects writes the batch with any additional side effects"""
    return batch.Write()
