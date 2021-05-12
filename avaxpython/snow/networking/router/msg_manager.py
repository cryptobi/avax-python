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

from avaxpython.ids.ShortID import ShortID

# DefaultMaxNonStakerPendingMsgs is the default number of messages that can be taken from
# the shared message pool by a single node
DefaultMaxNonStakerPendingMsgs = 20

# DefaultStakerPortion is the default portion of resources to reserve for stakers
DefaultStakerPortion = 0.375


class MsgManager:
    """# MsgManager manages incoming messages. It should be called when an incoming message
    # is ready to be processed and when an incoming message is processed. We call the
    # message "pending" if it has been received but not processed.
    """
    # AddPending marks that there is a message from [vdr] ready to be processed.
    # Returns true if the message will eventually be processed.
    def AddPending(self, idx: ShortID) -> bool:
        pass

    # Called when we process a message from the given peer
    def RemovePending(idx: ShortID):
        pass

    def Utilization(idx: ShortID) -> float:
        pass



class msgManager(MsgManager):
    
    def __init__(self, log, vdrs, mnspm, pm, rm, mt, scp, ct, c, m) -> None:
        super().__init__()
        self.log = log
        self.vdrs = vdrs
        self.maxNonStakerPendingMsgs=mnspm
        self.poolMessages = pm
        self.reservedMessages = rm
        self.msgTracker = mt
        self.stakerCPUPortion = scp
        self.cpuTracker = ct
        self.clock = c
        self.metrics = m

