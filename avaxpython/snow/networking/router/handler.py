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

import sys
import time
from typing import List
from avaxpython.snow.networking.router.service_queue import MultiLevelQueue
from avaxpython.snow.networking.router.message import Message
from avaxpython.utils import constants
from avaxpython.ids.ID import ID
from avaxpython.ids.ShortID import ShortID
from avaxpython.snow.engine.common.engine import Engine as CommonEngine


class Handler:
    """Handler receives messages from the network chain router and passes them onto the correct consensus engine"""
    def __init__(self, engine=None, ctx=None):   
        self.cpuTracker = None        
        self.msgManager = None            
        self.msgSema = None
        self.engine = engine
        self.serviceQueue = MultiLevelQueue()
        self.engine = engine
        self.ctx = ctx        

    def handle_message(self, msg: Message):

        if msg.messageType == constants.NotifyMsg:
            self.engine.Notify(msg.notification)
        elif msg.messageType == constants.GossipMsg:
            self.engine.Gossip()
        elif msg.messageType == constants.GetAcceptedFrontierMsg:
            self.engine.GetAcceptedFrontier(msg.validatorID, msg.requestID)
        elif msg.messageType == constants.AcceptedFrontierMsg:
            self.engine.AcceptedFrontier(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.GetAcceptedFrontierFailedMsg:
            self.engine.GetAcceptedFrontierFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.GetAcceptedMsg:
            self.engine.GetAccepted(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.AcceptedMsg:
            self.engine.Accepted(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.GetAcceptedFailedMsg:
            self.engine.GetAcceptedFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.GetAncestorsMsg:
            self.engine.GetAncestors(msg.validatorID, msg.requestID, msg.containerID)

        elif msg.messageType == constants.GetAncestorsFailedMsg:
            self.engine.GetAncestorsFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.MultiPutMsg:
            self.engine.MultiPut(msg.validatorID, msg.requestID, msg.containers)

        elif msg.messageType == constants.GetMsg:
            self.engine.Get(msg.validatorID, msg.requestID, msg.containerID)

        elif msg.messageType == constants.GetFailedMsg:
            self.engine.GetFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.PutMsg:
            self.engine.Put(msg.validatorID, msg.requestID, msg.containerID, msg.container)

        elif msg.messageType == constants.PushQueryMsg:
            self.engine.PushQuery(msg.validatorID, msg.requestID, msg.containerID, msg.container)

        elif msg.messageType == constants.PullQueryMsg:
            self.engine.PullQuery(msg.validatorID, msg.requestID, msg.containerID)

        elif msg.messageType == constants.QueryFailedMsg:
            self.engine.QueryFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.ChitsMsg:
            self.engine.Chits(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.ConnectedMsg:
            self.engine.Connected(msg.validatorID)

        elif msg.messageType == constants.DisconnectedMsg:
            self.engine.Disconnected(msg.validatorID)

        else:
            raise Exception(f"Unknown message type: {msg.messageType}")


    def Context(self):
        """Context of this Handler"""
        return self.engine.Context()

    def Engine(self):
        """Engine returns the engine this handler dispatches to"""
        return self.engine

    def SetEngine(self, engine):
        """SetEngine sets the engine for this handler to dispatch to"""
        self.engine = engine

    def Initialize(self, engine: CommonEngine, validators, msgChan, maxPendingMsgs: int, maxNonStakerPendingMsgs: int, stakerMsgPortion, stakerCPUPortion: float, namespace: str, metrics, delay):
        """Initialize this consensus handler
        engine must be initialized before initializing the handler"""
        self.ctx = engine.Context()        
        self.reliableMsgsSema = None
        self.closed = None
        self.msgChan = msgChan
        self.validators = validators
        self.maxPendingMsgs = maxPendingMsgs
        self.maxNonStakerPendingMsgs = maxNonStakerPendingMsgs
        self.stakerMsgPortion = stakerMsgPortion
        self.stakerCPUPortion = stakerCPUPortion
        self.namespace = namespace
        self.metrics = metrics
        self.delay = delay

        # Defines the maximum current percentage of expected CPU utilization for
        # a message to be placed in the queue at the corresponding index
        self.consumptionRanges = [
            0.125,
            0.5,
            1,
            sys.float_info.max
        ]

        cpuInterval = 15 # s
        # Defines the percentage of CPU time allotted to processing messages
        # from the bucket at the corresponding index.
        self.consumptionAllotments = [
            cpuInterval / 4,
            cpuInterval / 4,
            cpuInterval / 4,
            cpuInterval / 4,
        ]


    def Put(self, validatorID, requestID, containerID, container):
        
        return self.handle_message(Message(
            messageType=constants.PutMsg,
            validatorID=validatorID,
            requestID=requestID,
            containerID=containerID,
            container=container,
            received=int(time.time())
        ))

    
    def GetAcceptedFrontier(self, validatorID: ShortID, requestID: int, deadline: int):
        return self.handle_message(Message(
            messageType=constants.GetAcceptedFrontierMsg,
            validatorID=validatorID,
            requestID=requestID,
            deadline=deadline,
            received=int(time.time())
        ))
    
    def AcceptedFrontier(self, validatorID: ShortID, requestID: int, containerIDs: List[ID]):
        return self.handle_message(Message(
            messageType=constants.AcceptedFrontierMsg,
            validatorID=validatorID,
            requestID=requestID,
            containerIDs=containerIDs,
            received=int(time.time())
        ))

    def GetAcceptedFrontierFailed(self, validatorID: ShortID, requestID: int):
        return self.handle_message(Message(
            messageType=constants.GetAcceptedFrontierMsg,
            validatorID=validatorID,
            requestID=requestID,
            received=int(time.time())
        ))

    def GetAccepted(self, validatorID: ShortID, requestID: int, deadline: int, containerIDs: List[ID]):
        return self.handle_message(Message(
            messageType=constants.GetAcceptedMsg,
            validatorID=validatorID,
            requestID=requestID,
            deadline=deadline,
            containerIDs=containerIDs,
            received=int(time.time())
        ))
    
    def Accepted(self, validatorID: ShortID, requestID: int, containerIDs: List[ID]):
        return self.handle_message(Message(
            messageType=constants.AcceptedMsg,
            validatorID=validatorID,
            requestID=requestID,
            containerIDs=containerIDs,
            received=int(time.time())
        ))

    def GetAcceptedFailed(self, validatorID: ShortID, requestID: int):
        return self.handle_message(Message(
            messageType=constants.GetAcceptedFailedMsg,
            validatorID=validatorID,
            requestID=requestID,
            received=int(time.time())
        ))

    def GetAncestors(self, validatorID: ShortID, requestID: int, deadline: int, containerID: ID):
        return self.handle_message(Message(
            messageType=constants.GetAncestorsMsg,
            validatorID=validatorID,
            requestID=requestID,
            deadline=deadline,
            containerID=containerID,
            received=int(time.time())
        ))
    
    def MultiPut(self, validatorID: ShortID, requestID: int, containers: List[bytes]):
        return self.handle_message(Message(
            messageType=constants.MultiPutMsg,
            validatorID=validatorID,
            requestID=requestID,
            containers=containers,
            received=int(time.time())
        ))

    def GetAncestorsFailed(self, validatorID: ShortID, requestID: int):
        return self.handle_message(Message(
            messageType=constants.GetAncestorsFailedMsg,
            validatorID=validatorID,
            requestID=requestID,
            received=int(time.time())
        ))

    def Get(self, validatorID: ShortID, requestID: int, deadline: int, containerID: ID):
        return self.handle_message(Message(
            messageType=constants.GetMsg,
            validatorID=validatorID,
            requestID=requestID,
            deadline=deadline,
            containerID=containerID,
            received=int(time.time())
        ))
    
    def GetFailed(self, validatorID: ShortID, requestID: int):
        return self.handle_message(Message(
            messageType=constants.GetFailedMsg,
            validatorID=validatorID,
            requestID=requestID,
            received=int(time.time())
        ))

    def PushQuery(self, validatorID: ShortID, requestID: int, deadline: int, containerID: ID, container: bytes):
        return self.handle_message(Message(
            messageType=constants.PushQueryMsg,
            validatorID=validatorID,
            requestID=requestID,
            deadline=deadline,
            containerID=containerID,
            container=container,
            received=int(time.time())
        ))

    def PullQuery(self, validatorID: ShortID, requestID: int, deadline: int, containerID: ID):
        return self.handle_message(Message(
            messageType=constants.PullQueryMsg,
            validatorID=validatorID,
            requestID=requestID,
            deadline=deadline,
            containerID=containerID,
            received=int(time.time())
        ))
    
    def Chits(self, validatorID: ShortID, requestID: int, votes: List[ID]):
        return self.handle_message(Message(
            messageType=constants.ChitsMsg,
            validatorID=validatorID,
            requestID=requestID,
            containers=votes,
            received=int(time.time())
        ))

    def QueryFailed(self, validatorID: ShortID, requestID: int):
        return self.handle_message(Message(
            messageType=constants.QueryFailedMsg,
            validatorID=validatorID,
            requestID=requestID,
            received=int(time.time())
        ))

    def Connected(self, validatorID: ShortID):
        pass

    def Disconnected(self, validatorID: ShortID):
        pass

    def Gossip(self):
        pass

    def Notify(self, msg: int):
        pass

    def Shutdown(self):
        pass

    