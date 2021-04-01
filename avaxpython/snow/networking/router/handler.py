# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--

from .service_queue import MultiLevelQueue
from .message import Message
from avaxpython.utils import constants
import time

class Handler:

    def __init__(self):
        self.chains = {} # map[ids.ID]*Handler
        self.serviceQueue = MultiLevelQueue()

    def Put(self, validatorID, requestID, containerID, container):
        return self.serviceQueue.PushMessage(Message(
            messageType=constants.PutMsg,
            validatorID=validatorID,
            requestID=requestID,
            containerID=containerID,
            container=container,
            received=int(time.time())
        ))

    def handle_message(h, msg):

        if msg.messageType == constants.NotifyMsg:
            h.engine.Notify(msg.notification)
        elif msg.messageType == constants.GossipMsg:
            h.engine.Gossip()
        elif msg.messageType == constants.GetAcceptedFrontierMsg:
            h.engine.GetAcceptedFrontier(msg.validatorID, msg.requestID)
        elif msg.messageType == constants.AcceptedFrontierMsg:
            h.engine.AcceptedFrontier(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.GetAcceptedFrontierFailedMsg:
            h.engine.GetAcceptedFrontierFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.GetAcceptedMsg:
            h.engine.GetAccepted(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.AcceptedMsg:
            h.engine.Accepted(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.GetAcceptedFailedMsg:
            h.engine.GetAcceptedFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.GetAncestorsMsg:
            h.engine.GetAncestors(msg.validatorID, msg.requestID, msg.containerID)

        elif msg.messageType == constants.GetAncestorsFailedMsg:
            h.engine.GetAncestorsFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.MultiPutMsg:
            h.engine.MultiPut(msg.validatorID, msg.requestID, msg.containers)

        elif msg.messageType == constants.GetMsg:
            h.engine.Get(msg.validatorID, msg.requestID, msg.containerID)

        elif msg.messageType == constants.GetFailedMsg:
            h.engine.GetFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.PutMsg:
            h.engine.Put(msg.validatorID, msg.requestID, msg.containerID, msg.container)

        elif msg.messageType == constants.PushQueryMsg:
            h.engine.PushQuery(msg.validatorID, msg.requestID, msg.containerID, msg.container)

        elif msg.messageType == constants.PullQueryMsg:
            h.engine.PullQuery(msg.validatorID, msg.requestID, msg.containerID)

        elif msg.messageType == constants.QueryFailedMsg:
            h.engine.QueryFailed(msg.validatorID, msg.requestID)

        elif msg.messageType == constants.ChitsMsg:
            h.engine.Chits(msg.validatorID, msg.requestID, msg.containerIDs)

        elif msg.messageType == constants.ConnectedMsg:
            h.engine.Connected(msg.validatorID)

        elif msg.messageType == constants.DisconnectedMsg:
            h.engine.Disconnected(msg.validatorID)

        else:
            raise Exception(f"Unknown message type {msg.messageType}")