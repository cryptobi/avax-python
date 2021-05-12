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

import os
import os.path
import time
import avaxpython
from avaxpython.network.codec import Codec
from avaxpython.Config import Config
from avaxpython.network.peer import Peer
from avaxpython.network.Msg import Msg
from avaxpython.network.Op import Op
from .Handler import Handler
from .PeerState import PeerState


class MessageDumper(Handler):

    """A network handler which dumps binary messages into sample-data/."""

    def __init__(self):
        self.Log = avaxpython.config().logger()
        self.peer_state = PeerState()

        if "AVAX_PYTHON_PATH" not in os.environ:
            self.Log.error("Please set AVAX_PYTHON_PATH environment variable. Run . setenv.sh")
            exit(1)

        self.data_dir = "{}/sample-data".format(os.environ['AVAX_PYTHON_PATH'])

        if not os.path.exists(self.data_dir):
            self.Log.error("Directory {} does not exist. Create it first.".format(self.data_dir))
            exit(1)

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
        opcode = msg[0]

        self.avaxpython.config().logger().debug("handle_msg called opcode {} with {} bytes from peer {}".format(opcode, len(msg), peer))
        fn = "{}/{}.bin".format(self.data_dir, str(time.time()))
        with open(fn, "wb") as f:
            f.write(msg)

        now = time.time()
        peer.lastReceived = int(now)
        peer.net.lastMsgReceivedTime = int(now)

        parsed_msg = Codec.Parse(msg)
        oph = self.__op_handlers[parsed_msg.op]

        if not oph:
            err_str = f"No handler for op {parsed_msg.op} received from peer {peer}: Msg {parsed_msg}"
            self.avaxpython.config().logger().error(err_str)
            raise Exception(err_str)

        oph(parsed_msg, peer)


    def get_version(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Responding get_version")
        peer.Version()

    def version(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped version")    
        self.peer_state.set_got_version(peer.id)

    def signed_version(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped signed_version")    

    def get_peerlist(self, msg: Msg, peer: Peer):
        """Returns a list of connected Peer objects."""
        self.avaxpython.config().logger().debug("Responding get_peerlist")                    
        peers = self.peer_state.list_connected()
        peer.PeerList(peers)

    def peerlist(self, msg: Msg, peer: Peer):
        """On receiving a Peers message, a node should compare the nodes appearing in the message
        to its own list of neighbors, and forge connections to any new nodes."""
        self.avaxpython.config().logger().debug("Dumped peerlist")    

    def signed_peerlist(self, msg: Msg, peer: Peer):
        """Handing signed_peerlist message"""
        self.avaxpython.config().logger().debug("Dumped signed_peerlist")

    def ping(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Responding ping")    
        peer.Pong()

    def pong(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped pong")    
        
    def get_accepted_frontier(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped get_accepted_frontier")            

    def accepted_frontier(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped accepted_frontier")    
        
    def get_accepted(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped get_accepted")    
        
    def accepted(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped accepted")    
        
    def get(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped get")    
        
    def get_ancestors(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped get_ancestors")    
        
    def put(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped put")    
        
    def multi_put(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped multi_put")    
        
    def push_query(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Dumped push_query")    
        
    def pull_query(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Handling pull_query")    
        
    def chits(self, msg: Msg, peer: Peer):
        self.avaxpython.config().logger().debug("Handling chits")    
        
