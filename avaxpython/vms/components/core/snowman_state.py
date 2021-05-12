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
from avaxpython.vms.components.state.state import State
from avaxpython.snow.consensus.snowman.block import Block as SnowmanBlock

errWrongType = TypeError("got unexpected type from database")

# state.Get(Db, IDTypeID, lastAcceptedID) == ID of last accepted block
lastAcceptedID = ID(b'last')

class SnowmanState(State):
    """SnowmanState is a wrapper around state.State
    In additions to the methods exposed by state.State,
    SnowmanState exposes a few methods needed for managing
    state in a snowman vm"""
    _avax_interface = True

    def __init__(self) -> None:
        super().__init__()

    def GetBlock(db, block_id) -> SnowmanBlock:
        pass
    
    def PutBlock(db, blk: SnowmanBlock):
        pass

    def GetLastAccepted(db) -> ID:
        pass

    def PutLastAccepted(db, block_id: ID):
        pass



class snowmanState:
    """implements SnowmanState"""
    def __init__(self) -> None:        
	    self.State = None
