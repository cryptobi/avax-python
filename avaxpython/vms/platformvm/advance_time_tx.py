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

from avaxpython.types import Uint64, Int64
from avaxpython.vms.components.avax.metadata import Metadata
from avaxpython.structured import AvaxStructured

class UnsignedAdvanceTimeTx(AvaxStructured):
    """# UnsignedAdvanceTimeTx is a transaction to increase the chain's timestamp.
    # When the chain's timestamp is updated (a AdvanceTimeTx is accepted and
    # followed by a commit block) the staker set is also updated accordingly.
    # It must be that:
    #   * proposed timestamp > [current chain time]
    #   * proposed timestamp <= [time for next staker to be removed]
    """
    _avax_tags = [
        ("Time", { "serialize": True, "json": "time"}),
    ]
    def __init__(self) -> None:
            
        self.Metadata = Metadata()

        # Unix time this block proposes increasing the timestamp to
        self.Time = Uint64()


    # Timestamp returns the time this block is proposing the chain should be set to
    def Timestamp(self):
        return Int64(self.Time)


    def SemanticVerify(self, vm, db, stx):
        """SemanticVerify this transaction is valid."""
