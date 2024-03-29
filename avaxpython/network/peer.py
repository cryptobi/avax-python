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

import time
import avaxpython
from avaxpython.utils.ip import IPDesc
from avaxpython.network.Msg import Msg
from avaxpython.utils import constants
from avaxpython import Config


# alias is a secondary IP address where a peer
# was reached
class Alias:
    """Encapsulate an IP alias."""

    def __init__(self, ip, expiry):
        self.ip = ip
        self.expiry = expiry


class Peer:
    """Class encapsulating the functionality of an AVAX network Peer"""

    def __init__(self, net, conn, ip: IPDesc, tickerCloser=None, port=0, id=None, node=None, my_staking_ip = None):
        # network this peer is part of
        self.net = net
        self.expiry = None
        self.node = node
        # if the version message has been received and is valid. is only modified
        # on the connection's reader routine.
        self.gotVersion = False  # utils.AtomicBool
        self.gotPeerList = False  # utils.AtomicBool
        self.connected = False  # utils.AtomicBool

        # only close the peer once
        self.once = None  # sync.Once

        self.my_staking_ip = my_staking_ip

        # if the close function has been called.
        self.closed = False  # utils.AtomicBool

        # number of bytes currently in the send queue.
        self.pendingBytes = 0  # int64

        # lock to ensure that closing of the sender queue is handled safely
        self.senderLock = None  # sync.Mutex

        # queue of messages this connection is attempting to send the peer. Is
        # closed when the connection is closed.
        self.sender = None  # chan []byte

        # ip may or may not be set when the peer is first started. is only modified
        # on the connection's reader routine.
        self.ip: IPDesc = ip

        # ipLock must be held when accessing [ip].
        self.ipLock = None  # sync.RWMutex

        # aliases is a list of IPs other than [ip] that we have connected to
        # this peer at.
        self.aliases = []  # []alias

        # aliasTimer triggers the release of expired records from [aliases].
        self.aliasTimer = None  # *timer.Timer

        # aliasLock must be held when accessing [aliases] or [aliasTimer].
        self.aliasLock = None  # sync.Mutex

        # id should be set when the peer is first created.
        self.id = id

        # the connection object that is used to read/write messages from
        self.conn = conn

        # version that the peer reported during the handshake
        self.versionStruct = None
        self.versionStr = None  # utils.AtomicInterface

        # unix time of the last message sent and received respectively
        # Must only be accessed atomically
        self.lastSent = None
        self.lastReceived = None

        self.tickerCloser = tickerCloser

        # ticker processes
        self.tickerOnce = None  # sync.Once


        self.Log = avaxpython.config().logger()

    def __repr__(self):
        return f"IP {self.ip} ID {self.id}"

    # assume the [stateLock] is held
    def Start(p):
        # go p.ReadMessages()
        # go p.WriteMessages()
        pass

    def StartTicker(p):
        # go p.requestFinishHandshake()
        # go p.sendPings()
        # go p.monitorAliases()
        pass

    def sendPings(p):
        sendPingsTicker = time.NewTicker(p.net.pingFrequency)
        # defer sendPingsTicker.Stop()
        pass

        # request missing handshake messages from the peer

    def requestFinishHandshake(p):
        # finishHandshakeTicker = time.NewTicker(p.net.getVersionTimeout)
        # defer finishHandshakeTicker.Stop()
        pass

        # while True:

        # select {
        # case <-finishHandshakeTicker.C:

        #    if connected || closed {
        #        return
        #    }

        #    if !gotVersion {
        #        p.GetVersion()
        #    }
        #    if !gotPeerList {
        #        p.GetPeerList()
        #    }
        # case <-p.tickerCloser:
        #    return
        # }

    # monitorAliases periodically attempts
    # to release timed out alias IPs of the
    # peer.
    # monitorAliases will acquire [stateLock]
    # when an alias is released.
    def monitorAliases(p):
        # go func() {
        #    <-p.tickerCloser
        #    p.aliasTimer.Stop()
        # }()

        # p.aliasTimer.Dispatch()
        pass

    # attempt to read messages from the peer
    def ReadMessages(p):
        pass

    # attempt to write messages to the peer
    def WriteMessages(p):
        pass

    def Send(p, msg: Msg):

        bts = msg.Bytes()
        btlen = len(bts)
        barr = bytearray(btlen.to_bytes(4, "big"))
        barr.extend(bts)
        b_out = bytes(barr)
        b_sent = 0
        while b_sent < len(b_out):
            sent = p.conn.send(b_out[b_sent:])

            if sent == 0:
                raise RuntimeError(f"Cannot write {len(b_out[b_sent:])} bytes to peer {p} : Msg {msg}")

            b_sent += sent

        p.Log.debug(f"Sent {b_sent} bytes to Peer {p} : Msg {msg}")

        return b_sent == len(b_out)

    def handle(p, msg):
        pass

    def dropMessagePeer(p):
        pass

    def dropMessage(p, connPendingLen, networkPendingLen):
        pass

    def Close(p):
        pass

    def GetVersion(p):
        pass

    def Version(p):
        ts = int(time.time())

        msg = p.net.b.Version(constants.MainnetID, p.net.nodeID, ts, p.my_staking_ip, Config.AVAX_NETWORK_VERSION)

        p.Send(msg)

    def GetPeerList(p):
        pass

    def SendPeerList(p):
        pass

    def PeerList(p, peers):
        """Sends a peerlist message based on a list of Peer objects."""
        peer_ips = []
        for connected_peer in peers:
            for peer in p.net.peers.values():
                if connected_peer.id == peer.id:
                    peer_ips.append(peer.ip)

        msg = p.net.b.PeerList(peer_ips)
        p.Send(msg)

    def PeerListByIds(p, peerids):
        """Sends a peerlist based on a list of peer ids"""
        peer_ips = []
        for pid in peerids:
            for peer in p.net.peers.values():
                if pid == peer.id:
                    peer_ips.append(peer.ip)

        msg = p.net.b.PeerList(peer_ips)
        p.Send(msg)

    def Ping(p):
        pass

    def Pong(p):
        pass

    def getVersion(p, m):
        pass

    def version(p, msg):
        pass

    def getPeerList(p, msg):
        pass

    def peerList(msg):
        pass

    def ping(p, msg):
        p.Pong()

    def pong(p, msg):
        pass

    def getAcceptedFrontier(p, msg):
        pass

    def acceptedFrontier(p, msg):
        pass

    def getAccepted(p, msg):
        pass

    def accepted(p, msg):
        pass

    def get(p, msg):
        pass

    def getAncestors(p, msg):
        pass

    def put(p, msg):
        pass

    def multiPut(p, msg):
        pass

    def pushQuery(p, msg):
        pass

    def pullQuery(p, msg):
        pass

    def chits(p, msg):
        pass

    def tryMarkConnected(p):
        p.connected = True

    def discardIP(p):
        pass

    def discardMyIP(p):
        pass

    def setIP(p, ip):
        p.ip = ip

    def getIP(p):
        return p.ip

    def addAlias(p, ip):
        pass

    def releaseNextAlias(p, now_time):
        """releaseNextAlias returns the next released alias or None if none was released.
        If none was released, then this will schedule the next time to remove an alias."""

    def releaseExpiredAliases(p):
        """releaseExpiredAliases frees expired IP aliases. If there is an IP pending
        expiration, then the expiration is scheduled."""

    def releaseAllAliases(p):
        """releaseAllAliases frees all alias IPs.
        assumes [stateLock] is held and that [aliasTimer] has been stopped"""
        pass
