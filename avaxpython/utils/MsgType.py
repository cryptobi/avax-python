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


class MsgType():
    
    NullMsg = 0
    GetAcceptedFrontierMsg = 1
    AcceptedFrontierMsg = 2
    GetAcceptedFrontierFailedMsg = 3
    GetAcceptedMsg = 4
    AcceptedMsg = 5
    GetAcceptedFailedMsg = 6
    GetMsg = 7
    PutMsg = 8
    GetFailedMsg = 9
    PushQueryMsg = 10
    PullQueryMsg = 11
    ChitsMsg = 12
    QueryFailedMsg = 13
    ConnectedMsg = 14
    DisconnectedMsg = 15
    NotifyMsg = 16
    GossipMsg = 17
    GetAncestorsMsg = 18
    MultiPutMsg = 19
    GetAncestorsFailedMsg = 20
    
    __str_map = {
        NullMsg: "Null Message",
        GetAcceptedFrontierMsg: "Get Accepted Frontier Message",
        AcceptedFrontierMsg: "Accepted Frontier Message",
        GetAcceptedFrontierFailedMsg: "Get Accepted Frontier Failed Message",
        GetAcceptedMsg: "Get Accepted Message",
        AcceptedMsg: "Accepted Message",
        GetAcceptedFailedMsg: "Get Accepted Failed Message",
        GetMsg: "Get Message",
        GetAncestorsMsg: "Get Ancestors Message",
        GetAncestorsFailedMsg: "Get Ancestors Failed Message",
        PutMsg: "Put Message",
        MultiPutMsg: "MultiPut Message",
        GetFailedMsg: "Get Failed Message",
        PushQueryMsg: "Push Query Message",
        PullQueryMsg: "Pull Query Message",
        ChitsMsg: "Chits Message",
        QueryFailedMsg: "Query Failed Message",
        ConnectedMsg: "Connected Message",
        DisconnectedMsg: "Disconnected Message",
        NotifyMsg: "Notify Message",
        GossipMsg: "Gossip Message"
    }

    def str(self, tp):
        return self.__str_map.get(tp, f"Unknown Message Type: {tp}")    

