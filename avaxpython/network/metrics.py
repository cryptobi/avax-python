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


class messageMetrics:

    def __init__(self):
        self.numSent = 0
        self.numFailed = 0
        self.numReceived = 0
        self.prometheus.Counter = 0

    def initialize(msgType, registerer):
        #mm.numSent = prometheus.NewCounter(prometheus.CounterOpts(Namespace = constants.PlatformName,            Name = fmt.Sprintf("%s_sent", msgType),            Help = fmt.Sprintf("Number of %s messages sent", msgType))
        #mm.numFailed = prometheus.NewCounter(prometheus.CounterOpts(Namespace = constants.PlatformName,            Name = fmt.Sprintf("%s_failed", msgType),            Help = fmt.Sprintf("Number of %s messages that failed to be sent", msgType))
        #mm.numReceived = prometheus.NewCounter(prometheus.CounterOpts(Namespace = constants.PlatformName,            Name = fmt.Sprintf("%s_received", msgType),            Help = fmt.Sprintf("Number of %s messages received", msgType))

        err = registerer.Register(mm.numSent)
        if err != nil:
            return fmt.Errorf("failed to register sent statistics of %s due to %s", msgType, err)
        
        err = registerer.Register(mm.numFailed)
        if err != nil:
            return fmt.Errorf("failed to register failed statistics of %s due to %s", msgType, err)
        
        err = registerer.Register(mm.numReceived)
        if err != nil:
            return fmt.Errorf("failed to register received statistics of %s due to %s", msgType, err)
        
        return nil
    


class metrics:
    
    def __init__(self):
        self.numPeers = 0
        self.getVersion = 0
        self.version = 0
        self.getPeerlist = 0
        self.peerlist = 0
        self.ping = 0
        self.pong = 0
        self.getAcceptedFrontier = 0
        self.acceptedFrontier = 0
        self.getAccepted = 0
        self.accepted = 0
        self.get = 0
        self.getAncestors = 0
        self.put = 0
        self.multiPut = 0
        self.pushQuery = 0
        self.pullQuery = 0
        self.chits = 0
        self.messageMetrics = 0

    def initialize(registerer):

        m.numPeers = prometheus.NewGauge(prometheus.GaugeOpts(Namespace=constants.PlatformName, Name="peers", Help="Number of network peers"))

        errs = wrappers.Errs()
        err = registerer.Register(m.numPeers)
        if err != nil:
            errs.Add(fmt.Errorf("failed to register peers statistics due to %s", err))
        
        errs.Add(
            m.getVersion.initialize(GetVersion, registerer),
            m.version.initialize(Version, registerer),
            m.getPeerlist.initialize(GetPeerList, registerer),
            m.peerlist.initialize(PeerList, registerer),
            m.ping.initialize(Ping, registerer),
            m.pong.initialize(Pong, registerer),
            m.getAcceptedFrontier.initialize(GetAcceptedFrontier, registerer),
            m.acceptedFrontier.initialize(AcceptedFrontier, registerer),
            m.getAccepted.initialize(GetAccepted, registerer),
            m.accepted.initialize(Accepted, registerer),
            m.get.initialize(Get, registerer),
            m.getAncestors.initialize(GetAncestors, registerer),
            m.put.initialize(Put, registerer),
            m.multiPut.initialize(MultiPut, registerer),
            m.pushQuery.initialize(PushQuery, registerer),
            m.pullQuery.initialize(PullQuery, registerer),
            m.chits.initialize(Chits, registerer),
        )
        return errs.Err
    

    def message(msgType):
        
        if msgType == GetVersion:
            return m.getVersion
        if msgType == Version:
            return m.version
        if msgType == GetPeerList:
            return m.getPeerlist
        if msgType == PeerList:
            return m.peerlist
        if msgType == Ping:
            return m.ping
        if msgType == Pong:
            return m.pong
        if msgType == GetAcceptedFrontier:
            return m.getAcceptedFrontier
        if msgType == AcceptedFrontier:
            return m.acceptedFrontier
        if msgType == GetAccepted:
            return m.getAccepted
        if msgType == Accepted:
            return m.accepted
        if msgType == Get:
            return m.get
        if msgType == GetAncestors:
            return m.getAncestors
        if msgType == Put:
            return m.put
        if msgType == MultiPut:
            return m.multiPut
        if msgType == PushQuery:
            return m.pushQuery
        if msgType == PullQuery:
            return m.pullQuery
        if msgType == Chits:
            return m.chits
        
            return nil
        
    
