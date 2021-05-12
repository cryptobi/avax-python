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
import sys
import avaxpython
from avaxpython.network.codec import Codec
from avaxpython.Config import Config
from avaxpython.network.peer import Peer
from avaxpython.network.Msg import Msg
from avaxpython.network.Op import Op
from avaxpython.network.Field import Field 
from .Handler import Handler
from .PeerState import PeerState
from avaxpython.ids.ID import ID

class AVAX(Handler):

    """A network handler which attempts to implement the AVAX network protocol as described in https://docs.avax.network/build/references/network-protocol"""

    def __init__(self):
        self.Log = avaxpython.config().logger()
        self.peer_state = PeerState()

        self.__op_handlers =  {
            Op.GetVersion: self.get_version,
            Op.Version: self.version,
            Op.GetPeerList: self.get_peerlist,
            Op.PeerList: self.peerlist,
            Op.Ping: self.ping,
            Op.Pong: self.pong,
            Op.GetAcceptedFrontier: self.get_accepted_frontier,
            Op.AcceptedFrontier: self.accepted_frontier,
            Op.GetAccepted: self.get_accepted,
            Op.Accepted: self.accepted,
            Op.Get: self.get,
            Op.GetAncestors: self.get_ancestors,
            Op.Put: self.put,
            Op.MultiPut: self.multi_put,
            Op.PushQuery: self.push_query,
            Op.PullQuery: self.pull_query,
            Op.Chits: self.chits,
            Op.SignedVersion: self.signed_version,
            Op.SignedPeerList: self.signed_peerlist
        }

    def handle_msg(self, msg: bytes, peer: Peer):
        now = time.time()
        peer.lastReceived = int(now)
        peer.net.lastMsgReceivedTime = int(now)

        parsed_msg = Codec.Parse(msg)

        self.Log.debug(parsed_msg)
        oph = self.__op_handlers[parsed_msg.op]

        if not oph:
            err_str = f"No handler for op {parsed_msg.op} received from peer {peer}: Msg {parsed_msg}"
            avaxpython.config().logger().error(err_str)
            raise ValueError(err_str)

        oph(parsed_msg, peer)

    def get_version(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling get_version : Msg {} Peer {}".format(msg, peer))
        peer.Version()

    def version(self, msg: Msg, peer: Peer):
        """If the versions are incompatible or the current times differ too much, the connection will be terminated."""
        avaxpython.config().logger().debug("Handling version : Msg {} Peer {}".format(msg, peer))    
        self.peer_state.set_got_version(peer.id)

    def signed_version(self, msg: Msg, peer: Peer):
        """Handled signed_version message."""
        avaxpython.config().logger().debug("Handling signed_version : Msg {} Peer {}".format(msg, peer))    
        self.peer_state.set_got_version(peer.id)

    def get_peerlist(self, msg: Msg, peer: Peer):
        """Returns a list of connected Peer objects."""
        avaxpython.config().logger().debug("Handling get_peerlist : Msg {} Peer {}".format(msg, peer))    
        peers = self.peer_state.list_connected()
        peer.PeerList(peers)

    def peerlist(self, msg: Msg, peer: Peer):
        """On receiving a Peers message, a node should compare the nodes appearing in the message
        to its own list of neighbors, and forge connections to any new nodes."""
        avaxpython.config().logger().debug("Handling peerlist : Msg {} Peer {}".format(msg, peer))    
        self.peer_state.set_got_peerlist(peer.id)

    def signed_peerlist(self, msg: Msg, peer: Peer):
        """Handing signed_peerlist message"""
        avaxpython.config().logger().debug("Handling signed_peerlist : Msg {} Peer {}".format(msg, peer))    
        self.peer_state.set_got_peerlist(peer.id)

    def ping(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling ping : Msg {} Peer {}".format(msg, peer))    
        peer.Pong()

    def pong(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling pong : Msg {} Peer {}".format(msg, peer))    

    def createRequestID(self, validator_id, chain_id, request_id):
        """Generate a unique random ID for a requiest."""

    def get_accepted_frontier(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling get_accepted_frontier : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        deadline = int(peer.net.clock.time() + msg.fields[Field.Deadline])
        peer.net.router.GetAcceptedFrontier(peer.id, chain_id, request_id, deadline)
        
    def accepted_frontier(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling accepted_frontier : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container_ids = msg.fields[Field.ContainerIDs]
        peer.net.router.AcceptedFrontier(chain_id, request_id, container_ids)
        
    def get_accepted(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling get_accepted : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container_ids = msg.fields[Field.ContainerIDs]
        deadline = msg.fields[Field.Deadline]
        peer.net.router.GetAccepted(chain_id, request_id, deadline, container_ids)
        
    def accepted(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling accepted : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container_ids = msg.fields[Field.ContainerIDs]
        peer.net.router.Accepted(chain_id, request_id, container_ids)
        
    def get(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling get : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container_id = ID(msg.fields[Field.ContainerID])
        deadline = msg.fields[Field.Deadline]
        peer.net.router.Get(peer.id, chain_id, request_id, deadline, container_id)
        
    def get_ancestors(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling get_ancestors : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container_id = ID(msg.fields[Field.ContainerID])
        deadline = msg.fields[Field.Deadline]
        peer.net.router.GetAncestors(peer.id, chain_id, request_id, deadline, container_id)
        
    def put(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling put : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container = msg.fields[Field.ContainerBytes]
        container_id = ID(msg.fields[Field.ContainerID])
        peer.net.router.Put(peer.id, chain_id, request_id, container_id, container)

    def multi_put(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling multi_put : Msg {} Peer {}".format(msg, peer))  
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        containers = msg.fields[Field.MultiContainerBytes]
        peer.net.router.MultiPut(peer.id, chain_id, request_id, containers)
        
    def push_query(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling push_query : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container_id = ID(msg.fields[Field.ContainerID])
        container = msg.fields[Field.ContainerBytes]
        deadline = msg.fields[Field.Deadline]
        peer.net.router.PushQuery(peer.id, chain_id, request_id, deadline, container_id, container)

    def pull_query(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling pull_query : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        container_id = ID(msg.fields[Field.ContainerID])
        deadline = msg.fields[Field.Deadline]
        peer.net.router.PullQuery(chain_id, request_id, deadline, container_id)
        
    def chits(self, msg: Msg, peer: Peer):
        avaxpython.config().logger().debug("Handling chits : Msg {} Peer {}".format(msg, peer))    
        chain_id = ID(msg.fields[Field.ChainID])
        request_id = msg.fields[Field.RequestID]
        votes = msg.fields[Field.ContainerIDs]
        peer.net.router.Chits(chain_id, request_id, votes)
        
