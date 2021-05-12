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

from avaxpython.types import Bool
from avaxpython.ids.ID import ID
from avaxpython.structured import AvaxStructured

errShouldBeDSValidator = Exception("expected validator to be in the primary network")
errWrongTxType         = Exception("wrong transaction type")

class UnsignedRewardValidatorTx(AvaxStructured):
    """UnsignedRewardValidatorTx is a transaction that represents a proposal to
    remove a validator that is currently validating from the validator set.

    If this transaction is accepted and the next block accepted is a Commit
    block, the validator is removed and the address that the validator specified
    receives the staked AVAX as well as a validating reward.

    If this transaction is accepted and the next block accepted is an Abort
    block, the validator is removed and the address that the validator specified
    receives the staked AVAX but no reward."""
    _avax_tags = [
        ("TxID", { "serialize": True, "json": "txID"}),
    ]

    def __init__(self) -> None:
        
        avax.Metadata

        # ID of the tx that created the delegator/validator being removed/rewarded
        TxID = ID()

        # Marks if this validator should be rewarded according to this node.
        self.shouldPreferCommit = Bool()


    def SemanticVerify(self, vm, db, stx):
        """SemanticVerify this transaction performs a valid state transition.
        # The current validating set must have at least one member.
        # The next validator to be removed must be the validator specified in this block.
        # The next validator to be removed must be have an end time equal to the current
        #   chain timestamp."""


