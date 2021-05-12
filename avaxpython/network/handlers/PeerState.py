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

from avaxpython.network.Op import Op as AVAXOps

class PeerState:

    """Peer state helper class for AVAX handler implementations."""

    _state_vars = [
        "connected", "got_version", "got_peerlist", 
        "banned", "sent_peerlist", "sent_version"
    ]

    # message counts
    _numeric_vars = AVAXOps.OpNames()

    def __init__(self):
        self.peer_state = {}
        self.peer_stats = {}
        self.peers = []

    def get(self, peer_id, it):

        if peer_id not in self.peer_state:
            return None

        if it in self.peer_state[peer_id]:
            return self.peer_state[peer_id][it]

        return None

    def set(self, peer_id, it, v):
        if it not in PeerState._state_vars:
            raise Exception(f"Attempting to set invalid peer state variable {it}. Available vars: {PeerState._state_vars}")

        if peer_id not in self.peer_state:
            self.peer_state[peer_id] = {}

        self.peer_state[peer_id][it] = v
        
        return self.peer_state[peer_id][it]

    def increment(self, peer_id, it):
        if it not in PeerState._numeric_vars:
            raise Exception(f"Attempting to increment invalid numeric variable {it}. Available vars: {PeerState._numeric_vars}")

        if peer_id not in self.peer_stats:
            self.peer_stats[peer_id] = {}

        if it not in self.peer_stats[peer_id]:
            self.peer_stats[peer_id][it] = 0

        self.peer_stats[peer_id][it] += 1
        
        return self.peer_stats[peer_id][it]

    def set_connected(self, peer_id):
        self.set(peer_id, "connected", True)
        return self.get(peer_id, "connected")

    def set_got_version(self, peer_id):
        self.set(peer_id, "got_version", True)
        return self.get(peer_id, "got_version")

    def set_got_peerlist(self, peer_id):
        self.set(peer_id, "got_peerlist", True)
        return self.get(peer_id, "got_peerlist")

    def set_sent_version(self, peer_id):
        self.set(peer_id, "sent_version", True)
        return self.get(peer_id, "sent_version")

    def set_sent_peerlist(self, peer_id):
        self.set(peer_id, "sent_peerlist", True)
        return self.get(peer_id, "sent_peerlist")

    def get_sent_version(self, peer_id):        
        return self.get(peer_id, "sent_version")

    def get_sent_peerlist(self, peer_id):        
        return self.get(peer_id, "sent_peerlist")

    def get_connected(self, peer_id):
        return self.get(peer_id, "connected")

    def get_got_version(self, peer_id):        
        return self.get(peer_id, "got_version")

    def get_got_peerlist(self, peer_id):
        return self.get(peer_id, "got_peerlist")

    def set_banned(self, peer_id):
        self.set(peer_id, "banned", True)
        return self.get(peer_id, "banned")        

    def get_banned(self, peer_id):
        self.set(peer_id, "banned", True)
        return self.get(peer_id, "banned")

    def got_handshake(self, peer_id):
        return self.get_connected(peer_id) and self.get_got_version(peer_id) and self.get_got_peerlist(peer_id)

    def sent_handshake(self, peer_id):
        return self.get_connected(peer_id) and self.get_sent_version(peer_id) and self.get_sent_peerlist(peer_id)

    def list_connected(self):
        ret = []
        for id in self.peer_state:
            if "connected" in self.peer_state[id] and self.peer_state[id]["connected"]:
                for p in self.peers:
                    if p.id == id:
                        ret.append(p)

        return ret
