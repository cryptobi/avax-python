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


from .Op import Op
from .Field import Field

class Builder:

    # GetVersion message
    @classmethod
    def GetVersion(cls):
        return cls.Pack(Op.GetVersion)

    # Version message
    @classmethod
    def Version(cls, networkID, nodeID, myTime, ip, myVersion):
        return cls.Pack(Op.Version, {
            Field.NetworkID:  networkID,
            Field.NodeID:     nodeID,
            Field.MyTime:     myTime,
            Field.IP:         ip,
            Field.VersionStr: myVersion,
        })

    # GetPeerList message
    @classmethod
    def GetPeerList():
        return cls.Pack(Op.GetPeerList)

    # PeerList message
    @classmethod
    def PeerList(ipDescs):
        return cls.Pack(Op.PeerList, {Peers: ipDescs})

    # Ping message
    @classmethod
    def Ping(): 
        return cls.Pack(Op.Ping, nil)

    # Pong message
    @classmethod
    def Pong(): 
        return cls.Pack(Op.Pong, nil)

    # GetAcceptedFrontier message
    @classmethod
    def GetAcceptedFrontier(chainID, requestID, deadline):
        return cls.Pack(Op.GetAcceptedFrontier, {
            Field.ChainID:   chainID[:],
            Field.RequestID: requestID,
            Field.Deadline:  deadline,
        })

    # AcceptedFrontier message
    @classmethod
    def AcceptedFrontier(chainID, requestID, containerIDs):
        containerIDBytes = []
        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]
        

        return cls.Pack(Op.AcceptedFrontier, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.ContainerIDs: containerIDBytes,
        })

    # GetAccepted message
    @classmethod
    def GetAccepted(chainID, requestID, deadline, containerIDs):
        containerIDBytes = []
        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]
        
        return cls.Pack(Op.GetAccepted, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.Deadline:     deadline,
            Field.ContainerIDs: containerIDBytes,
        })

    # Accepted message
    @classmethod
    def Accepted(chainID, requestID, containerIDs):
        containerIDBytes = []

        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]

        return cls.Pack(Op.Accepted, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.ContainerIDs: containerIDBytes,
        })

    # GetAncestors message
    @classmethod
    def GetAncestors(chainID, requestID, deadline, containerID):
        return cls.Pack(Op.GetAncestors, {
            Field.ChainID:     chainID[:],
            Field.RequestID:   requestID,
            Field.Deadline:    deadline,
            Field.ContainerID: containerID[:],
        })

    # MultiPut message
    @classmethod
    def MultiPut(chainID, requestID, containers):
        return cls.Pack(Op.MultiPut, {
            Field.ChainID:             chainID[:],
            Field.RequestID:           requestID,
            Field.MultiContainerBytes: containers,
        })

    # Get message
    @classmethod
    def Get(chainID, requestID, deadline, containerID):
        return cls.Pack(Op.Get, {
            Field.ChainID:     chainID[:],
            Field.RequestID:   requestID,
            Field.Deadline:    deadline,
            Field.ContainerID: containerID[:],
        })
    

    # Put message
    @classmethod
    def Put(chainID, requestID, containerID, container):
        return cls.Pack(Op.Put, {
            Field.ChainID:        chainID[:],
            Field.RequestID:      requestID,
            Field.ContainerID:    containerID[:],
            Field.ontainerBytes: container,
        })

    # PushQuery message
    @classmethod
    def PushQuery(chainID, requestID, deadline, containerID, container):
        return cls.Pack(Op.PushQuery, {
            Field.ChainID:        chainID[:],
            Field.RequestID:      requestID,
            Field.Deadline:       deadline,
            Field.ContainerID:    containerID[:],
            Field.ContainerBytes: container,
        })

    # PullQuery message
    @classmethod
    def PullQuery(chainID, requestID, deadline, containerID):
        return cls.Pack(Op.PullQuery, {
            Field.ChainID:     chainID[:],
            Field.RequestID:   requestID,
            Field.Deadline:    deadline,
            Field.ContainerID: containerID[:],
        })

    # Chits message
    @classmethod
    def Chits(chainID, requestID, containerIDs):
        containerIDBytes = []
        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]
        
        return cls.Pack(Op.Chits, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.ContainerIDs: containerIDBytes,
        })
