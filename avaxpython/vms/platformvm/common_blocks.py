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
from avaxpython.vms.platformvm.block import Block
from avaxpython.vms.components.core.block import Block as CoreBlock
from avaxpython.structured import AvaxStructured

errInvalidBlockclass = TypeError("invalid block type")

class decision:
    """A decision block (either Commit, Abort, or DecisionBlock.) represents a
    decision to either commit (accept) or abort (reject) the changes specified in
    its parent, if its parent is a proposal. Otherwise, the changes are committed
    immediately."""
    def onAccept(self):
        """	This function should only be called after Verify is called.
        returns a database that contains the state of the chain if this block is
        accepted."""


class CommonBlock(AvaxStructured):
    """CommonBlock contains the fields common to all blocks of the Platform Chain"""
    _avax_tags = [
        ("Block", { "serialize": True}),
    ]
    def __init__(self) -> None:
        
        self.Block = CoreBlock()
        self.vm = None # Do not initialize VM here.

        # This block's children
        self.children = Slice()


class CommonDecisionBlock(AvaxStructured):
    """CommonDecisionBlock contains the fields and methods common to all decision blocks"""
    _avax_tags = [
        ("CommonBlock", { "serialize": True}),
    ]
    def __init__(self) -> None:    
        self.CommonBlock = CommonBlock()

        # state of the chain if this block is accepted
        self.onAcceptDB = None

        # to be executed if this block is accepted
        self.onAcceptFunc = None


class SingleDecisionBlock(AvaxStructured):
    """SingleDecisionBlock contains the accept for standalone decision blocks"""
    _avax_tags = [
        ("CommonDecisionBlock", { "serialize": True}),
    ]
    def __init__(self) -> None:    

	    self.CommonDecisionBlock = CommonDecisionBlock


class DoubleDecisionBlock(AvaxStructured):
    """DoubleDecisionBlock contains the accept for a pair of blocks"""
    _avax_tags = [
        ("CommonDecisionBlock", { "serialize": True}),
    ]
    def __init__(self) -> None:    
	    self.CommonDecisionBlock = CommonDecisionBlock()

