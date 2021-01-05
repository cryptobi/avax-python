# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

class MsgType(Enum):
    
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

