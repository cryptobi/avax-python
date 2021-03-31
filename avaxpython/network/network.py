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

import time
import socket
import hashlib
from .Builder import Builder
from .metrics import metrics as mt
import avaxpython.utils.logging
from ..ids import ShortID
from avaxpython.utils.timer import Executor
from avaxpython.utils import constants, ip
from avaxpython.utils import logging
from avaxpython.utils.ip import IPDesc
from avaxpython.ids.ShortID import ShortID
from avaxpython.ids.ID import ID
from avaxpython.version import version
from avaxpython.network.Messages import Messages
from avaxpython.network.peer import Peer
from avaxpython.network.Field import Field
from avaxpython.network.dialer import Dialer
from avaxpython.network.Op import Op
from avaxpython.utils.wrappers.Packer import Packer
from avaxpython import Config
import avaxpython
from avaxpython.network.handlers.AVAX import AVAX as AVAXHandler

# All periods in seconds
defaultInitialReconnectDelay = 1
defaultMaxReconnectDelay = 60 * 60
DefaultMaxMessageSize = 1 << 21
defaultMaxNetworkPendingSendBytes = 1 << 29  # 512MB
defaultNetworkPendingSendBytesToRateLimit = defaultMaxNetworkPendingSendBytes / 4
defaultMaxClockDifference = 60
defaultPeerListGossipSpacing = 60
defaultPeerListGossipSize = 100
defaultPeerListStakerGossipFraction = 2
defaultGetVersionTimeout = 2
defaultAllowPrivateIPs = True
defaultGossipSize = 50
defaultPingPongTimeout = 60
defaultPingFrequency = 3 * defaultPingPongTimeout / 4
defaultReadBufferSize = 16 * 1024
defaultReadHandshakeTimeout = 15
defaultConnMeterCacheSize = 10000


class Network:

    def __init__(self, id=None, ip=None, networkID=None, version=None, parser=None, listener=None, dialer=None,
                 serverUpgrader=None, clientUpgrader=None, vdrs=None, beacons=None, router=None, nodeID=None,
                 initialReconnectDelay=None, maxReconnectDelay=None, maxMessageSize=None, sendQueueSize=None,
                 maxNetworkPendingSendBytes=None, networkPendingSendBytesToRateLimit=None, maxClockDifference=None,
                 peerListGossipSpacing=None, peerListGossipSize=None, peerListStakerGossipFraction=None,
                 getVersionTimeout=None, allowPrivateIPs=None, gossipSize=None, pingPongTimeout=None,
                 pingFrequency=None, disconnectedIPs={}, connectedIPs={}, retryDelay=30, myIPs={}, peers={},
                 readBufferSize=None, readHandshakeTimeout=None, connMeter=None, connMeterMaxConns=None,
                 restartOnDisconnected=None, connectedCheckerCloser=None, disconnectedCheckFreq=None,
                 connectedMeter=None, restarter=None, apricotPhase0Time=None, avax_config=None, network_handler=None):

        self.avax_config = avax_config

        if network_handler is None:
            self.network_handler = AVAXHandler(self.avax_config)
        else:
            self.network_handler = network_handler

        self.futures = []  # manage network futures
        self.metrics = mt()
        self.id = id
        self.ip = ip
        self.networkID = networkID
        self.version = version
        self.parser = parser
        self.listener = listener
        self.dialer: Dialer = dialer
        self.serverUpgrader = serverUpgrader
        self.clientUpgrader = clientUpgrader
        self.vdrs = vdrs
        self.beacons = beacons
        self.router = router
        self.nodeID = nodeID
        self.clock = None  # TODO
        self.lastHeartbeat = 0
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
        self.connMeter = connectedMeter
        self.executor = avaxpython.parallel().executor()()
        self.b = Builder()
        self.apricotPhase0Time = apricotPhase0Time
        self.stateLock = None  # TODO sync.RWMutex
        self.pendingBytes = 0
        self.closed = False
        self.disconnectedIPs = disconnectedIPs
        self.connectedIPs = connectedIPs
        self.retryDelay = retryDelay
        self.myIPs = myIPs
        self.peers = peers
        self.closeOnce = None
        self.restartOnDisconnected = restartOnDisconnected
        self.connectedCheckerCloser = connectedCheckerCloser
        self.connectedMeter = connectedMeter
        self.disconnectedCheckFreq = disconnectedCheckFreq
        self.restarter = restarter
        self.hasMasked = True
        self.maskedValidators = {}
        self.Log = avax_config.logger()
        self.num_peers = 0

    def handle_protocol(self, peer):

        conn = peer.conn

        while True:

            #if not self.network_handler.peer_state.get_got_peerlist(peer.id):
            #    peer.GetPeerList()

            r = conn.recv(Config.DEFAULT_BUFFIZ)

            if not r:
                self.Log.error("Nothing received from {}. Aborting connection.".format(peer))
                break

            r_len = len(r)

            if r_len == Packer.IntLen:
                pak_len = int.from_bytes(r, "big")
                self.Log.debug("Attempting to read {} bytes".format(pak_len))
                try:
                    pak = conn.recv(pak_len)
                    if len(pak) == pak_len:
                        self.Log.debug("Received {} bytes.".format(pak_len))
                        self.network_handler.handle_msg(pak, peer)
                    else:
                        self.Log.warning(
                            "Expected message size {} and received size {} differ. Message ignored.".format(pak_len,
                                                                                                            len(pak)))

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    self.Log.error(f"Error receiving {pak_len} bytes from {peer} : {e}")

        self.Log.debug(f"Closing connection to {peer}")
        conn.close()

    def add_peer(self, peer: Peer):
        """Add a peer to our network state."""
        if self.peers == None:
            self.peers = []

        self.peers.append(peer)
        self.network_handler.peer_state.peers.append(peer)

        return self.peers

    def connect_peer(self, beacon_hp, beacon_id):
        self.Log.debug("Connecting to {} ID {}".format(beacon_hp, beacon_id))
        host_addr, host_port = beacon_hp.split(":")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = self.ssl_context.wrap_socket(s)
        conn.connect((host_addr, int(host_port)))
        self.handle_protocol(conn)

    def GetAcceptedFrontier(self, validatorIDs, chainID, requestID, deadline):

        msg = self.b.GetAcceptedFrontier(chainID, requestID, uint64(deadline.Sub(n.clock.Time())))

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
                self.Log.debug("failed to send GetAcceptedFrontier(%s, %s, %d)", vID, chainID, requestID)

                self.executor.Add(lambda: self.router.GetAcceptedFrontierFailed(vID, chainID, requestID))
                self.getAcceptedFrontier.numFailed.Inc()
            else:
                self.getAcceptedFrontier.numSent.Inc()

    def AcceptedFrontier(self, validatorID, chainID, requestID, containerIDs):
        msg = self.b.AcceptedFrontier(chainID, requestID, containerIDs)
        if err is not None:
            self.Log.error("failed to build AcceptedFrontier(%s, %d, %s): %s", chainID, requestID, containerIDs, err)
            return  # Packing message failed

        peer = self.getPeer(validatorID)
        if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
            self.Log.debug("failed to send AcceptedFrontier(%s, %s, %d, %s)", validatorID, chainID, requestID,
                           containerIDs)
            self.acceptedFrontier.numFailed.Inc()
        else:
            self.acceptedFrontier.numSent.Inc()

    def GetAccepted(self, validatorIDs, chainID, requestID, deadline, containerIDs):
        msg = self.b.GetAccepted(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerIDs)
        if err is not None:
            self.Log.error("failed to build GetAccepted(%s, %d, %s): %s", chainID, requestID, containerIDs, err)
            for validatorID in validatorIDs:
                vID = validatorID  # Prevent overwrite in next loop iteration
                self.executor.Add(lambda: self.router.GetAcceptedFailed(vID, chainID, requestID))

            return

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
                self.Log.debug("failed to send GetAccepted(%s, %s, %d, %s)", vID, chainID, requestID, containerIDs)
                self.executor.Add(lambda: self.router.GetAcceptedFailed(vID, chainID, requestID))
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
                self.Log.debug("skipping validator gossiping as no public validators are connected")
                continue

            msg = self.b.PeerList(ips)
            if err is not None:
                self.Log.error("failed to build peer list to gossip: %s. len(ips): %d", err, len(ips))
                continue

            stakers = []
            nonStakers = []
            for peer in allPeers:
                if self.vdrs.Contains(peer.id):
                    stakers = append(stakers, peer)
                else:
                    nonStakers = append(nonStakers, peer)

            numStakersToSend = (
                                           n.peerListGossipSize + self.peerListStakerGossipFraction - 1) / self.peerListStakerGossipFraction
            if len(stakers) < numStakersToSend:
                numStakersToSend = len(stakers)

            numNonStakersToSend = self.peerListGossipSize - numStakersToSend
            if len(nonStakers) < numNonStakersToSend:
                numNonStakersToSend = len(nonStakers)

            s = sampler.NewUniform()
            err = s.Initialize(uint64(len(stakers)))
            if err is not None:
                self.Log.error("failed to select stakers to sample: %s. len(stakers): %d", err, len(stakers))
                continue

            stakerIndices, err = s.Sample(numStakersToSend)
            if err is not None:
                self.Log.error("failed to select stakers to sample: %s. len(stakers): %d", err, len(stakers))
                continue

            for index in stakerIndices:
                stakers[int(index)].Send(msg)

            err = s.Initialize(uint64(len(nonStakers)))
            if err is not None:
                self.Log.error("failed to select non-stakers to sample: %s. len(nonStakers): %d", err, len(nonStakers))
                continue

            nonStakerIndices, err = s.Sample(numNonStakersToSend)
            if err is not None:
                self.Log.error("failed to select non-stakers to sample: %s. len(nonStakers): %d", err, len(nonStakers))
                continue

            for index in nonStakerIndices:
                nonStakers[int(index)].Send(msg)

    def Dispatch(self):

        # go self.gossip()

        # Continuously accept new connections
        while True:

            # Returns error when self.Close() is called
            conn = self.listener.accept()
            if conn is None:
                continue

            if self.closed:
                # network has been closed. exit loop
                return

            self.Log.debug("error during server accept: %s", err)
            return

            # spawn thread to handle connection
            #         

    def Accepted(self, validatorID, chainID, requestID, containerIDs):
        msg = self.b.Accepted(chainID, requestID, containerIDs)
        if err is not None:
            self.Log.error("failed to build Accepted(%s, %d, %s): %s", chainID, requestID, containerIDs, err)
            return  # Packing message failed

        peer = self.getPeer(validatorID)
        if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
            self.Log.debug("failed to send Accepted(%s, %s, %d, %s)", validatorID, chainID, requestID, containerIDs)
            self.accepted.numFailed.Inc()
        else:
            self.accepted.numSent.Inc()

    # GetAncestors implements the Sender interface.
    # assumes the stateLock is not held.
    def GetAncestors(self, validatorID, chainID, requestID, deadline, containerID):
        msg = self.b.GetAncestors(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID)
        if err is not None:
            self.Log.error("failed to build GetAncestors message: %s", err)
            return

        peer = self.getPeer(validatorID)
        if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
            self.Log.debug("failed to send GetAncestors(%s, %s, %d, %s)", validatorID, chainID, requestID, containerID)
            self.executor.Add(lambda: self.router.GetAncestorsFailed(validatorID, chainID, requestID))
            self.getAncestors.numFailed.Inc()
        else:
            self.getAncestors.numSent.Inc()

    # MultiPut implements the Sender interface.
    # assumes the stateLock is not held.
    def MultiPut(self, validatorID, chainID, requestID, containers):
        msg = self.b.MultiPut(chainID, requestID, containers)
        if err is not None:
            self.Log.error("failed to build MultiPut message because of container of size %d", len(containers))
            return

        peer = self.getPeer(validatorID)
        if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
            self.Log.debug("failed to send MultiPut(%s, %s, %d, %d)", validatorID, chainID, requestID, len(containers))
            self.multiPut.numFailed.Inc()
        else:
            self.multiPut.numSent.Inc()

    # Get implements the Sender interface.
    # assumes the stateLock is not held.
    def Get(self, validatorID, chainID, requestID, deadline, containerID):
        msg = self.b.Get(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID)
        self.Log.AssertNoError(err)

        peer = self.getPeer(validatorID)
        if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
            self.Log.debug("failed to send Get(%s, %s, %d, %s)", validatorID, chainID, requestID, containerID)
            self.executor.Add(lambda: self.router.GetFailed(validatorID, chainID, requestID))
            self.get.numFailed.Inc()
        else:
            self.get.numSent.Inc()

    # Put implements the Sender interface.
    # assumes the stateLock is not held.
    def Put(self, validatorID, chainID, requestID, containerID, container):
        msg = self.b.Put(chainID, requestID, containerID, container)
        if err is not None:
            self.Log.error("failed to build Put(%s, %d, %s): %s. len(container) : %d", chainID, requestID, containerID,
                           err, len(container))
            return

        peer = self.getPeer(validatorID)
        if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
            self.Log.debug("failed to send Put(%s, %s, %d, %s)", validatorID, chainID, requestID, containerID)
            self.Log.debug("container: %s", formatting.DumpBytes(Bytes=container))
            self.put.numFailed.Inc()
        else:
            self.put.numSent.Inc()

    # PushQuery implements the Sender interface.
    # assumes the stateLock is not held.
    def PushQuery(self, validatorIDs, chainID, requestID, deadline, containerID, container):
        msg = self.b.PushQuery(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID, container)

        if err is not None:
            self.Log.error("failed to build PushQuery(%s, %d, %s): %s. len(container): %d", chainID, requestID,
                           containerID, err, len(container))
            self.Log.debug("container: %s", formatting.DumpBytes(Bytes=container))
            for validatorID in validatorIDs:
                vID = validatorID  # Prevent overwrite in next loop iteration
                self.executor.Add(lambda: self.router.QueryFailed(vID, chainID, requestID))

            return  # Packing message failed

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
                self.Log.debug("failed to send PushQuery(%s, %s, %d, %s)", vID, chainID, requestID, containerID)
                self.Log.debug("container: %s", formatting.DumpBytes(Bytes=container))
                self.executor.Add(lambda: self.router.QueryFailed(vID, chainID, requestID))
                self.pushQuery.numFailed.Inc()
            else:
                self.pushQuery.numSent.Inc()

    # PullQuery implements the Sender interface.
    # assumes the stateLock is not held.
    def PullQuery(self, validatorIDs, chainID, requestID, deadline, containerID):
        msg = self.b.PullQuery(chainID, requestID, uint64(deadline.Sub(n.clock.Time())), containerID)
        self.Log.AssertNoError(err)

        for peerElement in self.getPeers(validatorIDs):
            peer = peerElement.peer
            vID = peerElement.id
            if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
                self.Log.debug("failed to send PullQuery(%s, %s, %d, %s)", vID, chainID, requestID, containerID)
                self.executor.Add(lambda: self.router.QueryFailed(vID, chainID, requestID))
            else:
                self.pullQuery.numSent.Inc()

    # Chits implements the Sender interface.
    # assumes the stateLock is not held.
    def Chits(self, validatorID, chainID, requestID, votes):
        msg = self.b.Chits(chainID, requestID, votes)
        if err is not None:
            self.Log.error("failed to build Chits(%s, %d, %s): %s", chainID, requestID, votes, err)
            return

        peer = self.getPeer(validatorID)
        if peer == None or not peer.connected.GetValue() or not peer.Send(msg):
            self.Log.debug("failed to send Chits(%s, %s, %d, %s)", validatorID, chainID, requestID, votes)
            self.chits.numFailed.Inc()
        else:
            self.chits.numSent.Inc()

    # Gossip attempts to gossip the container to the network
    # assumes the stateLock is not held.
    def Gossip(self, chainID, containerID, container):
        err = self.gossipContainer(chainID, containerID, container)
        if err is not None:
            self.Log.debug("failed to Gossip(%s, %s): %s", chainID, containerID, err)
            self.Log.debug("container:\n%s", formatting.DumpBytes(Bytes=container))

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

    def Close(self):

        self.Log.info("Shutting down network")

        self.listener.close()

        if self.closed:
            return

        peersToClose = self.peers.values()

        self.peers = {}

        for peer in peersToClose:
            peer.Close()

        self.closed = True

    def IP(self):
        return self.ip.IP()

    # assumes the stateLock is not held.
    def gossipContainer(self, chainID, containerID, container):

        msg = self.b.Put(chainID, constants.GossipMsgRequestID, containerID, container)

        if err is not None:
            return fmt.Errorf("attempted to pack too large of a Put message.\nContainer length: %d", len(container))

        allPeers = self.getAllPeers()

        numToGossip = self.gossipSize

        if numToGossip > len(allPeers):
            numToGossip = len(allPeers)

        s = sampler.NewUniform()

        err = s.Initialize(uint64(len(allPeers)))
        if err is not None:
            return err

        indices, err = s.Sample(numToGossip)

        if err is not None:
            return err

        for index in indices:
            if allPeers[int(index)].Send(msg):
                self.put.numSent.Inc()
            else:
                self.put.numFailed.Inc()

        return None

    def track(self, peer: Peer):
        """
        Track connection to a peer. This is different from the Go implementation which tracks an IPDesc. We track a peer.        
        """

        if self.closed:
            return

        if peer.ip.IP in self.disconnectedIPs and self.disconnectedIPs[peer.ip.IP]:
            return

        if peer.ip.IP in self.connectedIPs and self.connectedIPs[peer.ip.IP]:
            return

        if self.myIPs and peer.ip.IP in self.myIPs[peer.ip.IP]:
            return

        self.disconnectedIPs[peer.ip.IP] = None

        # avaxpython.parallel().go(self.connectTo, ip)
        self.connect_to(peer)

    # assumes the stateLock is not held. Only returns if the ip is connected to or
    # the network is closed
    def connect_to(self, peer: Peer):
        print(f"connecting to {peer.ip.IP}")

        while True:

            conn = self.attempt_connect(peer)
            if conn is None:
                self.Log.error(f"connect_to failed connecting to {ip} retrying in {self.retryDelay}s")
                time.sleep(self.retryDelay)

            self.handle_protocol(peer)

    @staticmethod
    def id_from_ip(ip: IPDesc):
        n = hashlib.new('ripemd160')
        n.update(bytes(str(ip), "utf-8"))
        return ShortID(n.digest())

    # assumes the stateLock is not held. Returns nil if a connection was able to be
    # established, or the network is closed.
    def attempt_connect(self, peer: Peer):

        self.Log.debug(f"Attempting to connect to {peer.ip}")

        conn = self.dialer.Dial(peer.ip)

        if conn is None:
            raise Exception(f"Cannot connect to {peer.ip}")

        peer.conn = conn
        peer.connected = True

        sid = Network.id_from_ip(peer.ip)
        peer.id = str(sid)

        self.tryAddPeer(peer)

        return conn

    # assumes the stateLock is not held. Returns an error if the peer couldn't be
    # added.
    def tryAddPeer(self, p):

        if self.closed:
            raise Exception("Network is closed.")

        self.peers[p.id] = p
        self.network_handler.peer_state.peers.append(p)
        self.network_handler.peer_state.set_connected(p.id)
        self.num_peers = len(self.peers)
        p.Start()

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
                if err is not None:
                    self.Log.error("failed to mask validator %s due to %s", p.id, err)
                else:
                    err = self.vdrs.RevealValidator(p.id)
                    if err is not None:
                        self.Log.error("failed to reveal validator %s due to %s", p.id, err)

                self.Log.debug("The new staking set is:\n%s", self.vdrs)
            else:
                peerVersion.Before(minimumUnmaskedVersion)
                self.maskeValidators.Add(p.id)
        else:
            self.maskedValidators.Remove(p.id)

        ip = p.getIP()
        self.Log.debug("connected to %s at %s", p.id, ip)

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

        self.Log.debug("disconnected from %s at %s", p.id, ip)

        delete(n.peers, p.id)
        self.num_peers.Set(float64(len(n.peers)))

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

        peers = make([] * PeerElement, validatorIDs.Len())
        i = 0
        for validatorID in validatorIDs:
            vID = validatorID  # Prevent overwrite in next loop iteration
            peers[i] = PeerElement(peer=self.peers[vID], id=vID)
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
                    if peer is not None and peer.connected.GetValue():
                        self.connectedMeter.Tick()
                        break

                self.stateLock.RUnlock()
                if self.connectedMeter.Ticks() != 0:
                    continue

                ticker.Stop()
                self.Log.Info("restarting node due to no peers")
                # go self.restarter.Restart()

            if readchannel(n.connectedCheckerCloser):
                ticker.Stop()
                return


def listener(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    bind_host = host
    if bind_host is None:
        bind_host = "0.0.0.0"

    s.bind((bind_host, port))
    s.listen()

    return s
