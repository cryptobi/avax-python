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
from avaxpython.ids.ID import ID
from avaxpython.snow.engine.common.config import Config as CommonConfig

# MaxContainersPerMultiPut is the maximum number of containers that can be
# sent in a MultiPut message
MaxContainersPerMultiPut = 2000

# StatusUpdateFrequency is how many containers should be processed between logs
StatusUpdateFrequency = 2500

# MaxOutstandingRequests is the maximum number of GetAncestors sent but not responded to/failed
MaxOutstandingRequests = 8

# MaxTimeFetchingAncestors is the maximum amount of time to spend fetching
# vertices during a call to GetAncestors
MaxTimeFetchingAncestors = 50 * 0.001


class Bootstrapper():
	
    def __init__(self, requestid, paf, af, sb, pa, av, st, we, ba, fafv, fav):

        self.RequestID = requestid

        # IDs of validators we have requested the accepted frontier from but haven't
        # received a reply from
        self.pendingAcceptedFrontier = paf
        self.acceptedFrontier = af

        # holds the beacons that were sampled for the accepted frontier
        self.sampledBeacons = sb
        self.pendingAccepted = pa
        self.acceptedVotes = av

        # current weight
        self.started = st
        self.weight = we

        # number of times the bootstrap was attempted
        self.bootstrapAttempts = ba

        # validators that failed to respond with their frontiers
        self.failedAcceptedFrontierVdrs = fafv

        # validators that failed to respond with their frontier votes
        self.failedAcceptedVdrs = fav



    def Initialize(b, config: CommonConfig):
        """Initialize implements the Engine interface."""
        b.Config = config
        b.Ctx.Log.Info("Starting bootstrap...")        

        beacons = b.Beacons.Sample(config.SampleK)

        err = b.sampledBeacons.Set(beacons)
        if err is not None:
            return err        

        for vdr in beacons:
            vdrID = vdr.ID()
            b.pendingAcceptedFrontier.Add(vdrID)
        
        for vdr in b.Beacons.List():
            vdrID = vdr.ID()
            b.pendingAccepted.Add(vdrID)    

        b.acceptedVotes = {}
        if b.Config.StartupAlpha > 0:
            return None        

        return b.Startup()

    def Startup(b):
        b.bootstrapAttempts += 1
        b.started = True
        
    def GetAcceptedFrontier(b, validatorID, requestID: int):
        pass
    
    def GetAcceptedFrontierFailed(b, validatorID, requestID: int):
        pass

    def AcceptedFrontier(validatorID, requestID: int, containerIDs: List[ID]):
        pass
    
    def GetAccepted(validatorID, requestID: int, containerIDs: List[ID]):
        pass

    # GetAcceptedFailed implements the Engine interface.
    def GetAcceptedFailed(validatorID, requestID: int):
        pass

    # Accepted implements the Engine interface.
    def Accepted(validatorID, requestID: int, containerIDs: List[ID]):
        pass

    # Connected implements the Engine interface.
    def Connected(validatorID):
        pass

    # Disconnected implements the Engine interface.
    def Disconnected(validatorID):
        pass

    def RestartBootstrap(reset: bool):
        pass