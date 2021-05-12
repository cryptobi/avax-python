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


# Op is an opcode
class Op:

    GetVersion = 0
    Version = 1
    GetPeerList = 2
    PeerList = 3
    Ping = 4
    Pong = 5
    # Bootstrapping:
    GetAcceptedFrontier = 6
    AcceptedFrontier = 7
    GetAccepted = 8
    Accepted = 9
    GetAncestors = 10
    MultiPut = 11
    # Consensus:
    Get = 12
    Put = 13
    PushQuery = 14
    PullQuery = 15
    Chits = 16
    SignedVersion = 17
    SignedPeerList = 18

    __op = {
        GetVersion: "get_version",
        Version: "version",
        GetPeerList: "get_peerlist",
        PeerList: "peerlist",
        Ping: "ping",
        Pong: "pong",
        GetAcceptedFrontier: "get_accepted_frontier",
        AcceptedFrontier: "accepted_frontier",
        GetAccepted: "get_accepted",
        Accepted: "accepted",
        Get: "get",
        GetAncestors: "get_ancestors",
        Put: "put",
        MultiPut: "multi_put",
        PushQuery: "push_query",
        PullQuery: "pull_query",
        Chits: "chits",
        SignedVersion: "signed_version",
        SignedPeerList: "signed_peer_list"
    }

    @classmethod
    def String(cls, op):
        if op in cls.__op: 
            return cls.__op.get(op)
    
        raise KeyError(f"Op {op} not found")


    @classmethod
    def OpNames(cls):
        return [cls.__op[x] for x in cls.__op]
        