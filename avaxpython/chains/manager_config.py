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

from avaxpython.vms.manager import Manager as AVMManager

class ManagerConfig:

    def __init__(self):
        self.StakingEnabled=False
        self.MaxPendingMsgs=0
        self.MaxNonStakerPendingMsgs=0
        self.StakerMSGPortion=0.0
        self.StakerCPUPortion=0.0
        self.Log=None
        self.VMManager=AVMManager()
        self.DecisionEvents=None
        self.ConsensusEvents=None
        self.DB=None
        self.Router=None
        self.Net=None
        self.ConsensusParams=None
        self.EpochFirstTransition=None
        self.EpochDuration=None
        self.Validators=None
        self.NodeID=None
        self.NetworkID=None
        self.Server=None
        self.Keystore=None
        self.AtomicMemory=None
        self.AVAXAssetID=None
        self.x_chain_id=None
        self.CriticalChains={}
        self.WhitelistedSubnets={}
        self.TimeoutManager=None
        self.HealthService=None
        self.RetryBootstrap=False
        self.RetryBootstrapMaxAttempts=0
