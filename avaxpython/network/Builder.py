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
from .codec import Codec

class Builder:

    def __init__(self):
        pass


    def GetVersion(self):
        return Codec.Pack(Op.GetVersion)

    
    def Version(self, networkID, nodeID, myTime, ip, myVersion):
        return Codec.Pack(Op.Version, {
            Field.NetworkID:  networkID,
            Field.NodeID:     nodeID,
            Field.MyTime:     myTime,
            Field.IP:         ip,
            Field.VersionStr: myVersion,
        })

    
    def GetPeerList():
        return Codec.Pack(Op.GetPeerList)

    
    def PeerList(ipDescs):
        return Codec.Pack(Op.PeerList, {Peers: ipDescs})

    
    def Ping(): 
        return Codec.Pack(Op.Ping, nil)

    
    def Pong(): 
        return Codec.Pack(Op.Pong, nil)

    # GetAcceptedFrontier message    
    def GetAcceptedFrontier(chainID, requestID, deadline):
        return Codec.Pack(Op.GetAcceptedFrontier, {
            Field.ChainID:   chainID[:],
            Field.RequestID: requestID,
            Field.Deadline:  deadline,
        })

    # AcceptedFrontier message    
    def AcceptedFrontier(chainID, requestID, containerIDs):
        containerIDBytes = []
        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]
        

        return Codec.Pack(Op.AcceptedFrontier, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.ContainerIDs: containerIDBytes,
        })

    # GetAccepted message    
    def GetAccepted(chainID, requestID, deadline, containerIDs):
        containerIDBytes = []
        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]
        
        return Codec.Pack(Op.GetAccepted, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.Deadline:     deadline,
            Field.ContainerIDs: containerIDBytes,
        })

    # Accepted message    
    def Accepted(chainID, requestID, containerIDs):
        containerIDBytes = []

        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]

        return Codec.Pack(Op.Accepted, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.ContainerIDs: containerIDBytes,
        })

    # GetAncestors message    
    def GetAncestors(chainID, requestID, deadline, containerID):
        return Codec.Pack(Op.GetAncestors, {
            Field.ChainID:     chainID[:],
            Field.RequestID:   requestID,
            Field.Deadline:    deadline,
            Field.ContainerID: containerID[:],
        })

    # MultiPut message    
    def MultiPut(chainID, requestID, containers):
        return Codec.Pack(Op.MultiPut, {
            Field.ChainID:             chainID[:],
            Field.RequestID:           requestID,
            Field.MultiContainerBytes: containers,
        })

    # Get message    
    def Get(chainID, requestID, deadline, containerID):
        return Codec.Pack(Op.Get, {
            Field.ChainID:     chainID[:],
            Field.RequestID:   requestID,
            Field.Deadline:    deadline,
            Field.ContainerID: containerID[:],
        })
    

    # Put message    
    def Put(chainID, requestID, containerID, container):
        return Codec.Pack(Op.Put, {
            Field.ChainID:        chainID[:],
            Field.RequestID:      requestID,
            Field.ContainerID:    containerID[:],
            Field.ontainerBytes: container,
        })

    # PushQuery message    
    def PushQuery(chainID, requestID, deadline, containerID, container):
        return Codec.Pack(Op.PushQuery, {
            Field.ChainID:        chainID[:],
            Field.RequestID:      requestID,
            Field.Deadline:       deadline,
            Field.ContainerID:    containerID[:],
            Field.ContainerBytes: container,
        })

    # PullQuery message    
    def PullQuery(chainID, requestID, deadline, containerID):
        return Codec.Pack(Op.PullQuery, {
            Field.ChainID:     chainID[:],
            Field.RequestID:   requestID,
            Field.Deadline:    deadline,
            Field.ContainerID: containerID[:],
        })

    # Chits message    
    def Chits(chainID, requestID, containerIDs):
        containerIDBytes = []
        for containerID in containerIDs:
            copy = containerID
            containerIDBytes[i] = copy[:]
        
        return Codec.Pack(Op.Chits, {
            Field.ChainID:      chainID[:],
            Field.RequestID:    requestID,
            Field.ContainerIDs: containerIDBytes,
        })
