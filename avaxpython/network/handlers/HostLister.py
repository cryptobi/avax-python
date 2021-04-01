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

from avaxpython.network.codec import Codec
from avaxpython.Config import Config
from avaxpython.network.peer import Peer
from avaxpython.network.Msg import Msg
from avaxpython.network.Op import Op
from .Handler import Handler
from .PeerState import PeerState

class HostLister(Handler):

    """A network handler which lists all peers it can find on the AVAX network."""

    def __init__(self, avax_config: Config):
        self.avax_config = avax_config
        self.Log = avax_config.logger()
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
            Op.Chits: self.chits
        }

    def handle_msg(self, msg: bytes, peer: Peer):        
        opcode = msg[0]

        self.avax_config.logger().debug("handle_msg called opcode {} with {} bytes from peer {}".format(opcode, len(msg), peer))

        parsed_msg = Codec.Parse(msg)
        self.Log.debug(parsed_msg)
        oph = self.__op_handlers[parsed_msg.op]

        if not oph:
            err_str = f"No handler for op {parsed_msg.op} received from peer {peer}: Msg {parsed_msg}"
            self.avax_config.logger().error(err_str)
            raise Exception(err_str)

        oph(parsed_msg, peer)

    def get_version(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling get_version : Msg {} Peer {}".format(msg, peer))
        peer.Version()

    def version(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling version : Msg {} Peer {}".format(msg, peer))    
        self.peer_state.set_got_version(peer.id)
        # If the versions are incompatible or the current times differ too much, the connection will be terminated.

    def get_peerlist(self, msg: Msg, peer: Peer):
        """Returns a list of connected Peer objects."""
        self.avax_config.logger().debug("Handling get_peerlist : Msg {} Peer {}".format(msg, peer))    
        peers = self.peer_state.list_connected()
        peer.PeerList(peers)

    def peerlist(self, msg: Msg, peer: Peer):
        """On receiving a Peers message, a node should compare the nodes appearing in the message
        to its own list of neighbors, and forge connections to any new nodes."""
        self.avax_config.logger().debug("Handling peerlist : Msg {} Peer {}".format(msg, peer))    
        for p in msg.fields[5]:
            print(p)
        self.peer_state.set_got_peerlist(peer.id)

    def ping(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling ping : Msg {} Peer {}".format(msg, peer))    
        peer.Pong()

    def pong(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling pong : Msg {} Peer {}".format(msg, peer))    
        
    def get_accepted_frontier(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling get_accepted_frontier : Msg {} Peer {}".format(msg, peer))    
        

    def accepted_frontier(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling accepted_frontier : Msg {} Peer {}".format(msg, peer))    
        
    def get_accepted(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling get_accepted : Msg {} Peer {}".format(msg, peer))    
        
    def accepted(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling accepted : Msg {} Peer {}".format(msg, peer))    
        
    def get(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling get : Msg {} Peer {}".format(msg, peer))    
        
    def get_ancestors(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling get_ancestors : Msg {} Peer {}".format(msg, peer))    
        
    def put(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling put : Msg {} Peer {}".format(msg, peer))    
        
    def multi_put(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling multi_put : Msg {} Peer {}".format(msg, peer))    
        
    def push_query(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling push_query : Msg {} Peer {}".format(msg, peer))    
        
    def pull_query(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling pull_query : Msg {} Peer {}".format(msg, peer))    
        
    def chits(self, msg: Msg, peer: Peer):
        self.avax_config.logger().debug("Handling chits : Msg {} Peer {}".format(msg, peer))    
        
