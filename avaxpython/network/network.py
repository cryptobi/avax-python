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


from .Builder import Builder
from .metrics import metrics as mt
import avaxpython.utils.logging
from ..ids import ShortID
from avaxpython.utils.timer import Executor
from avaxpython.utils import constants, ip
from avaxpython.utils.logging import logger
from avaxpython.utils import logging
from avaxpython.ids.ShortID import ShortID
from avaxpython.ids.ID import ID
from avaxpython.version import version

# All periods in seconds
defaultInitialReconnectDelay = 1
defaultMaxReconnectDelay = 60 * 60
DefaultMaxMessageSize = 1 << 21
defaultMaxNetworkPendingSendBytes = 1 << 29 # 512MB
defaultNetworkPendingSendBytesToRateLimit = defaultMaxNetworkPendingSendBytes / 4
defaultMaxClockDifference = 60
defaultPeerListGossipSpacing = 60
defaultPeerListGossipSize = 100
defaultPeerListStakerGossipFraction = 2
defaultGetVersionTimeout = 2
defaultAllowPrivateIPs = True
defaultGossipSize = 50
defaultPingPongTimeout  = 60
defaultPingFrequency = 3 * defaultPingPongTimeout / 4
defaultReadBufferSize = 16 * 1024
defaultReadHandshakeTimeout = 15
defaultConnMeterCacheSize = 10000


class Network:

    def __init__(self,log,id, ip,networkID,version,parser,listener,dialer,serverUpgrader,clientUpgrader,vdrs,beacons,router,nodeID,initialReconnectDelay,maxReconnectDelay,maxMessageSize,sendQueueSize,maxNetworkPendingSendBytes, networkPendingSendBytesToRateLimit,maxClockDifference,peerListGossipSpacing,peerListGossipSize,peerListStakerGossipFraction,getVersionTimeout,allowPrivateIPs,gossipSize,pingPongTimeout,pingFrequency,disconnectedIPs,connectedIPs,retryDelay,myIPs,peers,readBufferSize,readHandshakeTimeout,connMeter,connMeterMaxConns,restartOnDisconnected,connectedCheckerCloser,disconnectedCheckFreq,connectedMeter,restarter,apricotPhase0Time):
        self.log = log
        self.metrics = mt()
        self.id = id
        self.ip =  ip
        self.networkID = networkID
        self.version = version
        self.parser = parser
        self.listener = listener
        self.dialer = dialer
        self.serverUpgrader = serverUpgrader
        self.clientUpgrader = clientUpgrader
        self.vdrs = vdrs
        self.beacons = beacons
        self.router = router
        self.nodeID = nodeID
        self.clock = None # TODO 
        self.lastHeartbeat =  0
        self.initialReconnectDelay = initialReconnectDelay
        self.maxReconnectDelay = maxReconnectDelay
        self.maxMessageSize = maxMessageSize
        self.sendQueueSize = sendQueueSize
        self.maxNetworkPendingSendBytes = maxNetworkPendingSendBytes
        self.networkPendingSendBytesToRateLimit = networkPendingSendBytesToRateLimit
        self.maxClockDifference = maxClockDifference
        self.peerListGossipSpacing = peerListGossipSpacing
        self.peerListGossipSize = peerListGossipSize
        self.peerListStakerGossipFraction = peerListStakerGossipFraction
        self.getVersionTimeout = getVersionTimeout
        self.allowPrivateIPs = allowPrivateIPs
        self.gossipSize = gossipSize
        self.pingPongTimeout = pingPongTimeout
        self.pingFrequency = pingFrequency
        self.readBufferSize = readBufferSize
        self.readHandshakeTimeout = readHandshakeTimeout
        self.connMeterMaxConns = connMeterMaxConns
        self.connMeter = None # TODO 
        self.executor = None # TODO Executor()
        self.b = Builder()
        self.apricotPhase0Time = apricotPhase0Time
        self.stateLock = None # TODO sync.RWMutex
        self.pendingBytes = 0
        self.closed = False
        self.disconnectedIPs = {}
        self.connectedIPs = {}
        self.retryDelay = {}
        self.myIPs = {}
        self.peers = {}
        self.closeOnce = None
        self.restartOnDisconnected = restartOnDisconnected
        self.connectedCheckerCloser = connectedCheckerCloser
        self.connectedMeter = connectedMeter
        self.disconnectedCheckFreq = disconnectedCheckFreq
        self.restarter = restarter
        self.hasMasked = True
        self.maskedValidators = {}

        
    def GetAcceptedFrontier(self, validatorIDs, chainID, requestID, deadline):

        msg = self.b.GetAcceptedFrontier(chainID, requestID, uint64(deadline.Sub(n.clock.Time())))
        self.log.AssertNoError(err)

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
                self.log.Debug("failed to send GetAcceptedFrontier(%s, %s, %d)", vID, chainID, requestID)

                self.executor.Add(lambda : self.router.GetAcceptedFrontierFailed(vID, chainID, requestID) )
                self.getAcceptedFrontier.numFailed.Inc()
            else:
                self.getAcceptedFrontier.numSent.Inc()            
        
    
    def AcceptedFrontier(self, validatorID, chainID, requestID, containerIDs):
        msg = self.b.AcceptedFrontier(chainID, requestID, containerIDs)
        if err != nil: 
            self.log.Error("failed to build AcceptedFrontier(%s, %d, %s): %s", chainID, requestID, containerIDs, err)
            return # Packing message failed
        
        peer = self.getPeer(validatorID)
        if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
            self.log.Debug("failed to send AcceptedFrontier(%s, %s, %d, %s)", validatorID, chainID, requestID, containerIDs)
            self.acceptedFrontier.numFailed.Inc()
        else:
            self.acceptedFrontier.numSent.Inc()        
       

    def GetAccepted(self, validatorIDs, chainID, requestID, deadline, containerIDs):
        msg = self.b.GetAccepted(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerIDs)
        if err != nil:
            self.log.Error("failed to build GetAccepted(%s, %d, %s): %s", chainID, requestID, containerIDs, err)
            for validatorID in validatorIDs:
                vID = validatorID # Prevent overwrite in next loop iteration
                self.executor.Add(lambda : self.router.GetAcceptedFailed(vID, chainID, requestID))
            
            return        

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
                self.log.Debug("failed to send GetAccepted(%s, %s, %d, %s)", vID, chainID, requestID, containerIDs)
                self.executor.Add(lambda : self.router.GetAcceptedFailed(vID, chainID, requestID))
                self.getAccepted.numFailed.Inc()
            else:
                self.getAccepted.numSent.Inc()
            
            

    def gossip(self):

        t = time.NewTicker(n.peerListGossipSpacing)
        # # defer t.Stop()

        for _ in t.C:
            if self.closed.GetValue():
                return

            allPeers = self.getAllPeers()
            if len(allPeers) == 0:
                continue

            ips = []
            for peer in allPeers:
                ip = peer.getIP()
                if peer.connected.GetValue() and not ip.IsZero() and self.vdrs.Contains(peer.id):
                    peerVersion = (peer.versionStruct.GetValue())(version.Version)
                    if not peerVersion.Before(minimumUnmaskedVersion) or time.Since(n.apricotPhase0Time) < 0:
                        ips = append(ips, ip)

            if len(ips) == 0:
                self.log.Debug("skipping validator gossiping as no public validators are connected")
                continue
            
            msg = self.b.PeerList(ips)
            if err != nil:
                self.log.Error("failed to build peer list to gossip: %s. len(ips): %d", err, len(ips)) 
                continue
            
            stakers = []
            nonStakers = []
            for peer in allPeers:
                if self.vdrs.Contains(peer.id):
                    stakers = append(stakers, peer)
                else:
                    nonStakers = append(nonStakers, peer)
            

            numStakersToSend = (n.peerListGossipSize + self.peerListStakerGossipFraction - 1) / self.peerListStakerGossipFraction
            if len(stakers) < numStakersToSend:
                numStakersToSend = len(stakers)
            
            numNonStakersToSend = self.peerListGossipSize - numStakersToSend
            if len(nonStakers) < numNonStakersToSend:
                numNonStakersToSend = len(nonStakers)

            s = sampler.NewUniform()
            err = s.Initialize(uint64(len(stakers)))
            if err != nil:
                self.log.Error("failed to select stakers to sample: %s. len(stakers): %d", err, len(stakers))
                continue
            
            stakerIndices, err = s.Sample(numStakersToSend)
            if err != nil:
                self.log.Error("failed to select stakers to sample: %s. len(stakers): %d", err, len(stakers))
                continue
            
            for index in stakerIndices:
                stakers[int(index)].Send(msg)
            
            err = s.Initialize(uint64(len(nonStakers)))
            if err != nil:
                self.log.Error("failed to select non-stakers to sample: %s. len(nonStakers): %d", err, len(nonStakers))
                continue
            
            nonStakerIndices, err = s.Sample(numNonStakersToSend)
            if err != nil:
                self.log.Error("failed to select non-stakers to sample: %s. len(nonStakers): %d", err, len(nonStakers))
                continue
            
            for index in nonStakerIndices:
                nonStakers[int(index)].Send(msg)        


    def Dispatch(self):

        # go self.gossip()

        def _func():
            duration = time.Until(n.apricotPhase0Time)
            time.Sleep(duration)

            self.stateLock.Lock()
            # # defer self.stateLock.Unlock()

            self.hasMasked = true
            for vdrID in self.maskedValidators.List():
                err = self.vdrs.MaskValidator(vdrID)
                if err != nil:
                    self.log.Error("failed to mask validator %s due to %s", vdrID, err)
                        
            self.maskedValidators.Clear()
            self.log.Verbo("The new staking set is:\n%s", self.vdrs)
        
        # go _func

        # Continuously accept new connections
        while True:
            # Returns error when self.Close() is called
            conn, err = self.listener.Accept() 
            if err != nil:
                netErr, ok = (err)(net.Error)
                if ok and netErr.Temporary():
                    # Sleep for a small amount of time to try to wait for the
                    # temporary error to go away.
                    time.Sleep(time.Millisecond)
                    continue
                

                # When [n].Close() is called, [n.listener].Close() is called.
                # This causes [n.listener].Accept() to return an error.
                # If that happened, don't log/return an error here.
                if self.closed.GetValue():
                    return errNetworkClosed
                
                self.log.Debug("error during server accept: %s", err)
                return err
            
            conn, ok = (conn)(*net.TCPConn)
            if ok:
                err = conn.SetLinger(0)
                if err != nil:
                    self.log.Warn("failed to set no linger due to: %s", err)
                
                err = conn.SetNoDelay(true)
                if err != nil:
                    self.log.Warn("failed to set socket nodelay due to: %s", err)
                            

            addr = conn.RemoteAddr().String()
            ticks, err = self.connMeter.Register(addr)
            # looking for > self.connMeterMaxConns indicating the second tick
            if err == nil and ticks > self.connMeterMaxConns:
                self.log.Debug("connection from %s temporarily dropped", addr)
                _ = conn.Close()
                continue        

            def _func():
                channelx = None # TODO criar solucao para canais
                err = self.upgrade(peer(net = self,conn=conn, tickerCloser=channelx), self.serverUpgrader)
                if err != nil:
                    self.log.Verbo("failed to upgrade connection: %s", err)
                        
            # go _func
        
        

    def Accepted(self, validatorID, chainID, requestID, containerIDs):
        msg = self.b.Accepted(chainID, requestID, containerIDs)
        if err != nil:
            self.log.Error("failed to build Accepted(%s, %d, %s): %s", chainID, requestID, containerIDs, err)
            return # Packing message failed

        peer = self.getPeer(validatorID)
        if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
            self.log.Debug("failed to send Accepted(%s, %s, %d, %s)", validatorID, chainID, requestID, containerIDs)
            self.accepted.numFailed.Inc()
        else:
            self.accepted.numSent.Inc()
        

    # GetAncestors implements the Sender interface.
    # assumes the stateLock is not held.
    def GetAncestors(self, validatorID, chainID, requestID, deadline, containerID):
        msg = self.b.GetAncestors(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID)
        if err != nil:
            self.log.Error("failed to build GetAncestors message: %s", err)
            return

        peer = self.getPeer(validatorID)
        if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
            self.log.Debug("failed to send GetAncestors(%s, %s, %d, %s)", validatorID, chainID, requestID, containerID)
            self.executor.Add(lambda : self.router.GetAncestorsFailed(validatorID, chainID, requestID))
            self.getAncestors.numFailed.Inc()
        else:
            self.getAncestors.numSent.Inc()


    # MultiPut implements the Sender interface.
    # assumes the stateLock is not held.
    def MultiPut(self, validatorID, chainID, requestID, containers):
        msg = self.b.MultiPut(chainID, requestID, containers)
        if err != nil:
            self.log.Error("failed to build MultiPut message because of container of size %d", len(containers))
            return

        peer = self.getPeer(validatorID)
        if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
            self.log.Debug("failed to send MultiPut(%s, %s, %d, %d)", validatorID, chainID, requestID, len(containers))
            self.multiPut.numFailed.Inc()
        else:
            self.multiPut.numSent.Inc()
        

    # Get implements the Sender interface.
    # assumes the stateLock is not held.
    def Get(self, validatorID, chainID, requestID, deadline, containerID):
        msg = self.b.Get(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID)
        self.log.AssertNoError(err)

        peer = self.getPeer(validatorID)
        if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
            self.log.Debug("failed to send Get(%s, %s, %d, %s)", validatorID, chainID, requestID, containerID)
            self.executor.Add(lambda : self.router.GetFailed(validatorID, chainID, requestID) )
            self.get.numFailed.Inc()
        else:
            self.get.numSent.Inc()
    

    # Put implements the Sender interface.
    # assumes the stateLock is not held.
    def Put(self, validatorID, chainID, requestID, containerID, container):
        msg = self.b.Put(chainID, requestID, containerID, container)
        if err != nil:
            self.log.Error("failed to build Put(%s, %d, %s): %s. len(container) : %d", chainID, requestID, containerID, err, len(container))
            return

        peer = self.getPeer(validatorID)
        if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
            self.log.Debug("failed to send Put(%s, %s, %d, %s)", validatorID, chainID, requestID, containerID)
            self.log.Verbo("container: %s", formatting.DumpBytes(Bytes = container))
            self.put.numFailed.Inc()
        else:
            self.put.numSent.Inc()



    # PushQuery implements the Sender interface.
    # assumes the stateLock is not held.
    def PushQuery(self, validatorIDs, chainID, requestID, deadline, containerID, container):
        msg = self.b.PushQuery(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID, container)

        if err != nil:
            self.log.Error("failed to build PushQuery(%s, %d, %s): %s. len(container): %d", chainID, requestID, containerID, err, len(container))
            self.log.Verbo("container: %s", formatting.DumpBytes(Bytes=container))
            for validatorID in validatorIDs:
                vID = validatorID # Prevent overwrite in next loop iteration
                self.executor.Add(lambda : self.router.QueryFailed(vID, chainID, requestID))
            
            return # Packing message failed

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
                self.log.Debug("failed to send PushQuery(%s, %s, %d, %s)", vID, chainID, requestID, containerID)
                self.log.Verbo("container: %s", formatting.DumpBytes(Bytes = container))
                self.executor.Add(lambda : self.router.QueryFailed(vID, chainID, requestID))
                self.pushQuery.numFailed.Inc()
            else:
                self.pushQuery.numSent.Inc()
    

    # PullQuery implements the Sender interface.
    # assumes the stateLock is not held.
    def PullQuery(self, validatorIDs, chainID, requestID, deadline, containerID):
        msg = self.b.PullQuery(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID)
        self.log.AssertNoError(err)

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
                self.log.Debug("failed to send PullQuery(%s, %s, %d, %s)", vID, chainID, requestID, containerID)
                self.executor.Add(lambda : self.router.QueryFailed(vID, chainID, requestID))
            else:
                self.pullQuery.numSent.Inc()
            
        
    

    # Chits implements the Sender interface.
    # assumes the stateLock is not held.
    def Chits(self, validatorID, chainID, requestID, votes):
        msg = self.b.Chits(chainID, requestID, votes)
        if err != nil:
            self.log.Error("failed to build Chits(%s, %d, %s): %s", chainID, requestID, votes, err)
            return

        peer = self.getPeer(validatorID)
        if peer == nil or not peer.connected.GetValue() or not peer.Send(msg):
            self.log.Debug("failed to send Chits(%s, %s, %d, %s)", validatorID, chainID, requestID, votes)
            self.chits.numFailed.Inc()
        else:
            self.chits.numSent.Inc()
    

    # Gossip attempts to gossip the container to the network
    # assumes the stateLock is not held.
    def Gossip(self, chainID, containerID, container):
        err = self.gossipContainer(chainID, containerID, container)
        if err != nil:
            self.log.Debug("failed to Gossip(%s, %s): %s", chainID, containerID, err)
            self.log.Verbo("container:\n%s", formatting.DumpBytes(Bytes = container))        


    # Accept is called after every consensus decision
    # assumes the stateLock is not held.
    def Accept(self, ctx, containerID, container):
        if not ctx.IsBootstrapped():
            # don't gossip during bootstrapping
            return None

        return self.gossipContainer(ctx.ChainID, containerID, container)

    # heartbeat registers a new heartbeat to signal liveness
    def heartbeat(self):        
        # TODO atomic.StoreInt64(self.lastHeartbeat, self.clock.Time().Unix()) 
        pass

    # GetHeartbeat returns the most recent heartbeat time
    def GetHeartbeat(self):
        return atomic.LoadInt64(n.lastHeartbeat) 


    # IPs implements the Network interface
    # assumes the stateLock is not held.
    def Peers(self):
        self.stateLock.RLock()
        # # defer self.stateLock.RUnlock() # TODO

        peers = []
        for peer in self.peers:
            if peer.connected.GetValue():
                # TODO tem erro nesta linha
                # IP=peer.conn.RemoteAddr().String(),PublicIP=peer.getIP().String(),ID=peer.id.PrefixedString(constants.NodeIDPrefix),Version=(peer.versionStr.GetValue())(string),LastSent=time.Unix(atomic.LoadInt64(peer.lastSent), 0),LastReceived=time.Unix(atomic.LoadInt64(peer.lastReceived), 0
                p = PeerID()                
                peers.append(p)
                                
        return peers
    

    # Close implements the Network interface
    # assumes the stateLock is not held.
    def Close(self):
        self.closeOnce.Do(n.close)
        return None


    def close(self):

        self.log.Info("shutting down network")
        # Stop checking whether we're connected to peers.
        close(n.connectedCheckerCloser)

        err = self.listener.Close()
        if err != nil:
            self.log.Debug("closing network listener failed with: %s", err)

        if self.closed.GetValue():
            return

        self.stateLock.Lock()
        if self.closed.GetValue():
            self.stateLock.Unlock()
            return
        
        self.closed.SetValue(true)

        peersToClose = []
        i = 0
        for peer in self.peers:
            peersToClose[i] = peer
            i += 1

        self.peers = make(map[ids.ShortID]*peer)
        self.stateLock.Unlock()

        for peer in peersToClose:
            peer.Close() # Grabs the stateLock
    

    # Track implements the Network interface
    # assumes the stateLock is not held.
    def Track(self, ip):
        self.stateLock.Lock()
        # defer self.stateLock.Unlock()
        self.track(ip)


    def IP(self):
        return self.ip.IP()


    # assumes the stateLock is not held.
    def gossipContainer(self, chainID, containerID, container):

        msg = self.b.Put(chainID, constants.GossipMsgRequestID, containerID, container)

        if err != nil:
            return fmt.Errorf("attempted to pack too large of a Put message.\nContainer length: %d", len(container))
        
        allPeers = self.getAllPeers()

        numToGossip = self.gossipSize

        if numToGossip > len(allPeers):
            numToGossip = len(allPeers)        

        s = sampler.NewUniform()

        err = s.Initialize(uint64(len(allPeers)))
        if err != nil:
            return err        

        indices, err = s.Sample(numToGossip)
        
        if err != nil:
            return err

        for index in indices:
            if allPeers[int(index)].Send(msg):
                self.put.numSent.Inc()
            else:
                self.put.numFailed.Inc()
                    
        return None


    # assumes the stateLock is held.
    def track(self, ip):
        if self.closed.GetValue():
            return
        

        str = ip.String()
        _, ok = self.disconnectedIPs[str]
        if ok:
            return
        
        _, ok = self.connectedIPs[str]
        if ok:
            return
        
        _, ok = self.myIPs[str]
        if ok:
            return
        
        self.disconnectedIPs[str] = None

        # TODO
        #go self.connectTo(ip)
    



    # assumes the stateLock is not held. Only returns if the ip is connected to or
    # the network is closed
    def connectTo(self, ip):
        str = ip.String()
        self.stateLock.RLock()
        delay = self.retryDelay[str]
        self.stateLock.RUnlock()

        while True:
            time.Sleep(delay)

            if delay == 0:
                delay = self.initialReconnectDelay            

            # Randomization is only performed here to distribute reconnection
            # attempts to a node that previously shut down. This doesn't require
            # cryptographically secure random number generation.
            delay = None # TODO time.Duration(float64(delay) * (1 + rand.Float64())) # #nosec G404
            if delay > self.maxReconnectDelay:
                # set the timeout to [.75, 1) * maxReconnectDelay
                delay = None # TODO time.Duration(float64(n.maxReconnectDelay) * (3 + rand.Float64()) / 4) # #nosec G404            

            self.stateLock.Lock()
            _, isDisconnected = self.disconnectedIPs[str]
            _, isConnected = self.connectedIPs[str]
            _, isMyself = self.myIPs[str]
            closed = self.closed

            if not isDisconnected or isConnected or isMyself or closed.GetValue():
                # If the IP was discovered by the peer connecting to us, we don't
                # need to attempt to connect anymore
                # If the IP was discovered to be our IP address, we don't need to
                # attempt to connect anymore
                # If the network was closed, we should stop attempting to connect
                # to the peer

                self.stateLock.Unlock()
                return
            
            self.retryDelay[str] = delay
            self.stateLock.Unlock()

            err = self.attemptConnect(ip)
            if err == nil:
                return
            
            self.log.Verbo("error attempting to connect to %s: %s. Reattempting in %s", ip, err, delay)
    

    # assumes the stateLock is not held. Returns nil if a connection was able to be
    # established, or the network is closed.
    def attemptConnect(self, ip):
        self.log.Verbo("attempting to connect to %s", ip)

        conn, err = self.dialer.Dial(ip)
        if err != nil:
            return err
        
        conn, ok = (conn)(*net.TCPConn)
        if ok:
            err = conn.SetLinger(0)
            if err != nil:
                self.log.Warn("failed to set no linger due to: %s", err)
            
            err = conn.SetNoDelay(true)
            if err != nil:
                self.log.Warn("failed to set socket nodelay due to: %s", err)
            
        p1 = peer(net=self,ip=ip,conn=conn,tickerCloser=None)
        return self.upgrade(p1, self.clientUpgrader)
    

    # assumes the stateLock is not held. Returns an error if the peer's connection
    # wasn't able to be upgraded.
    def upgrade(self, p, upgrader):
        err = p.conn.SetReadDeadline(time.Now().Add(n.readHandshakeTimeout))
        if err != nil:
            _ = p.conn.Close()
            self.log.Verbo("failed to set the read deadline with %s", err)
            return err        

        id, conn, err = upgrader.Upgrade(p.conn)
        if err != nil:
            _ = p.conn.Close()
            self.log.Verbo("failed to upgrade connection with %s", err)
            return err

        err = conn.SetReadDeadline(time.Time())
        if err != nil:
            _ = p.conn.Close()
            self.log.Verbo("failed to clear the read deadline with %s", err)
            return err

        p.sender = make(chan, self.sendQueueSize)
        p.id = id
        p.conn = conn

        err = self.tryAddPeer(p)
        if err != nil:
            _ = p.conn.Close()
            self.log.Debug("dropping peer connection due to: %s", err)

        return None
    

    # assumes the stateLock is not held. Returns an error if the peer couldn't be
    # added.
    def tryAddPeer(self, p):
        self.stateLock.Lock()
        # defer self.stateLock.Unlock()

        ip = p.getIP()

        if self.closed.GetValue():
            # the network is closing, so make sure that no further reconnect
            # attempts are made.
            return errNetworkClosed        

        # if this connection is myself, then I should delete the connection and
        # mark the IP as one of mine.
        if p.id == self.id:
            if not ip.IsZero(): 
                # if self.ip is less useful than p.ip set it to this IP
                if self.ip.IP().IsZero():
                    self.log.Info("setting my ip to %s because I was able to connect to myself through this channel", p)
                
            ip.String()
            delete(n.disconnectedIPs, str)
            delete(n.retryDelay, str)                
            
            return errPeerIsMyself
        

        # If I am already connected to this peer, then I should close this new
        # connection.
        _, ok = self.peers[p.id]
        if ok:
            if not ip.IsZero():
                str = ip.String()
                delete(n.disconnectedIPs, str)
                delete(n.retryDelay, str)

            return fmt.Errorf("duplicated connection from %s at %s", p.id.PrefixedString(constants.NodeIDPrefix), ip)

        self.peers[p.id] = p
        self.numPeers.Set(float64(len(n.peers)))
        p.Start()

        return None
    

    # assumes the stateLock is not held. Returns the ips of connections that have
    # valid IPs that are marked as validators.
    def validatorIPs(self):
        self.stateLock.RLock()
        # defer self.stateLock.RUnlock()

        ips = []
        for peer in self.peers:
            ip = peer.getIP()
            if peer.connected.GetValue() and not ip.IsZero() and self.vdrs.Contains(peer.id):
                peerVersion = (peer.versionStruct.GetValue())(version.Version)
                if not peerVersion.Before(minimumUnmaskedVersion) or time.Since(n.apricotPhase0Time) < 0:
                    ips = append(ips, ip)
                                    
        return ips
    

    # should only be called after the peer is marked as connected. Should not be
    # called after disconnected is called with this peer.
    # assumes the stateLock is not held.
    def connected(self, p):
        p.net.stateLock.Lock()
        # defer p.net.stateLock.Unlock()

        p.connected.SetValue(true)

        peerVersion = (p.versionStruct.GetValue())(version.Version)

        # TODO indentacao quebrada neste setor
        if self.hasMasked:
                if peerVersion.Before(minimumUnmaskedVersion):
                    err = self.vdrs.MaskValidator(p.id)
                    if err != nil:
                        self.log.Error("failed to mask validator %s due to %s", p.id, err)
                    else:
                        err = self.vdrs.RevealValidator(p.id)
                        if err != nil:
                            self.log.Error("failed to reveal validator %s due to %s", p.id, err)
                        
                    self.log.Verbo("The new staking set is:\n%s", self.vdrs)
                else:
                    peerVersion.Before(minimumUnmaskedVersion)
                    self.maskeValidators.Add(p.id)
        else:
            self.maskedValidators.Remove(p.id)

        ip = p.getIP()
        self.log.Debug("connected to %s at %s", p.id, ip)

        if not ip.IsZero():
            str = ip.String()

            delete(n.disconnectedIPs, str)
            delete(n.retryDelay, str)
            self.connectedIPs[str] = None

        self.router.Connected(p.id)


    # should only be called after the peer is marked as connected.
    # assumes the stateLock is not held.
    def disconnected(self, p):
        p.net.stateLock.Lock()
        # defer p.net.stateLock.Unlock()

        ip = p.getIP()

        self.log.Debug("disconnected from %s at %s", p.id, ip)

        delete(n.peers, p.id)
        self.numPeers.Set(float64(len(n.peers)))

        if not ip.IsZero():
            str = ip.String()

            delete(n.disconnectedIPs, str)
            delete(n.connectedIPs, str)

            self.track(ip)        

        if p.connected.GetValue():
            self.router.Disconnected(p.id)
    


    def getPeers(self, validatorIDs):
        self.stateLock.RLock()
        # defer self.stateLock.RUnlock()

        if self.closed.GetValue():
            return None
        

        peers = make([]*PeerElement, validatorIDs.Len())
        i = 0
        for validatorID in validatorIDs:
            vID = validatorID # Prevent overwrite in next loop iteration
            peers[i] = PeerElement(peer= self.peers[vID], id=vID)
            i += 1
        

        return peers
    

    # Safe copy the peers. Assumes the stateLock is not held.
    def getAllPeers(self):
        self.stateLock.RLock()
        # defer self.stateLock.RUnlock()

        if self.closed.GetValue():
            return None

        peers = []
        i = 0
        for peer in self.peers:
            peers[i] = peer
            i += 1
        
        return peers
    

    # Safe find a single peer
    # assumes the stateLock is not held.
    def getPeer(self, validatorID):
        self.stateLock.RLock()
        # defer self.stateLock.RUnlock()

        if self.closed.GetValue():
            return None

        return self.peers[validatorID]
    

    # restartOnDisconnect checks every [n.disconnectedCheckFreq] whether this node is connected
    # to any peers. If the node is not connected to any peers for [disconnectedRestartTimeout],
    # restarts the node.
    def restartOnDisconnect(self):
        ticker = time.NewTicker(n.disconnectedCheckFreq)
        while True:

            if readchannel(ticker.C):

                if self.closed.GetValue():
                    return
                
                self.stateLock.RLock()
                for peer in self.peers:
                    if peer != nil and peer.connected.GetValue():
                        self.connectedMeter.Tick()
                        break
                    
                self.stateLock.RUnlock()
                if self.connectedMeter.Ticks() != 0:
                    continue
                
                ticker.Stop()
                self.log.Info("restarting node due to no peers")
                # go self.restarter.Restart()

            if readchannel(n.connectedCheckerCloser):
                ticker.Stop()
                return
    

# NewDefaultNetwork returns a new Network implementation with the provided
# parameters and some reasonable default values.
def NewDefaultNetwork(registerer, log, id, ip, networkID, version, parser, listener, dialer, serverUpgrader, clientUpgrader, vdrs, beacons, router, connMeterResetDuration, connMeterMaxConns, restarter, restartOnDisconnected, disconnectedCheckFreq, disconnectedRestartTimeout, apricotPhase0Time, sendQueueSize):
	return NewNetwork(
		registerer,
		log,
		id,
		ip,
		networkID,
		version,
		parser,
		listener,
		dialer,
		serverUpgrader,
		clientUpgrader,
		vdrs,
		beacons,
		router,
		defaultInitialReconnectDelay,
		defaultMaxReconnectDelay,
		DefaultMaxMessageSize,
		sendQueueSize,
		defaultMaxNetworkPendingSendBytes,
		defaultNetworkPendingSendBytesToRateLimit,
		defaultMaxClockDifference,
		defaultPeerListGossipSpacing,
		defaultPeerListGossipSize,
		defaultPeerListStakerGossipFraction,
		defaultGetVersionTimeout,
		defaultAllowPrivateIPs,
		defaultGossipSize,
		defaultPingPongTimeout,
		defaultPingFrequency,
		defaultReadBufferSize,
		defaultReadHandshakeTimeout,
		connMeterResetDuration,
		defaultConnMeterCacheSize,
		connMeterMaxConns,
		restarter,
		restartOnDisconnected,
		disconnectedCheckFreq,
		disconnectedRestartTimeout,
		apricotPhase0Time,
	)


# NewNetwork returns a new Network implementation with the provided parameters.
def NewNetwork(registerer, log, id, ip, networkID, version, parser, listener, dialer, serverUpgrader, clientUpgrader, vdrs, beacons, router, initialReconnectDelay, maxReconnectDelay, maxMessageSize, sendQueueSize, maxNetworkPendingSendBytes, networkPendingSendBytesToRateLimit, maxClockDifference, peerListGossipSpacing, peerListGossipSize, peerListStakerGossipFraction, getVersionTimeout, allowPrivateIPs, gossipSize, pingPongTimeout, pingFrequency, readBufferSize, readHandshakeTimeout, connMeterResetDuration, connMeterCacheSize, connMeterMaxConns, restarter, restartOnDisconnected, disconnectedCheckFreq, disconnectedRestartTimeout, apricotPhase0Time):

	netw = Network(
		log=log,
		id=id,
		ip=ip,
		networkID=networkID,
		version=version,
		parser=parser,
		listener=listener,
		dialer=dialer,
		serverUpgrader=serverUpgrader,
		clientUpgrader=clientUpgrader,
		vdrs=vdrs,
		beacons=beacons,
		router=router,
		nodeID=0, # TODO rand.Uint32(),
		initialReconnectDelay=initialReconnectDelay,
		maxReconnectDelay=maxReconnectDelay,
		maxMessageSize=0, # TODO int64(maxMessageSize),
		sendQueueSize=sendQueueSize,
		maxNetworkPendingSendBytes=0, # TODO int64(maxNetworkPendingSendBytes),
		networkPendingSendBytesToRateLimit=0, # TODO int64(networkPendingSendBytesToRateLimit),
		maxClockDifference=maxClockDifference,
		peerListGossipSpacing=peerListGossipSpacing,
		peerListGossipSize=peerListGossipSize,
		peerListStakerGossipFraction=peerListStakerGossipFraction,
		getVersionTimeout=getVersionTimeout,
		allowPrivateIPs=allowPrivateIPs,
		gossipSize=gossipSize,
		pingPongTimeout=pingPongTimeout,
		pingFrequency=pingFrequency,
		disconnectedIPs={},
		connectedIPs={},
		retryDelay={},
		myIPs={},
		peers={},
		readBufferSize=readBufferSize,
		readHandshakeTimeout=readHandshakeTimeout,
		connMeter=None, # TODO NewConnMeter(connMeterResetDuration, connMeterCacheSize),
		connMeterMaxConns=connMeterMaxConns,
		restartOnDisconnected=restartOnDisconnected,
		connectedCheckerCloser=None, # TODO channel
		disconnectedCheckFreq=disconnectedCheckFreq,
		connectedMeter=None, # TODO timer.TimedMeter{Duration: disconnectedRestartTimeout},
		restarter=restarter,
		apricotPhase0Time=apricotPhase0Time
    )

    # TODO metrics err = netw.initialize(registerer)
	# if err != nil:
	#	log.Warn("initializing network metrics failed with: %s", err)
	
	# TODO netw.executor.Initialize()
	# TODO go netw.executor.Dispatch()
	netw.heartbeat()

	if restartOnDisconnected and disconnectedCheckFreq != 0 and disconnectedRestartTimeout != 0:
		log.Info("node will restart if not connected to any peers")
		# pre-queue one tick to avoid immediate shutdown.
		netw.connectedMeter.Tick()
		# go netw.restartOnDisconnect()
	
	return netw
