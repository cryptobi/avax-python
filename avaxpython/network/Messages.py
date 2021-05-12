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



from .Op import Op
from .Field import Field

class Messages:
	"""
		Network message structures.
		Canonical version: avalanchego/network/commands.go
	"""
	__msg_structure = {
		# Handshake:
		Op.GetVersion:  [],
		Op.Version:     [Field.NetworkID, Field.NodeID, Field.MyTime, Field.IP, Field.VersionStr],
		Op.GetPeerList: [],
		Op.PeerList:    [Field.Peers],
		Op.Ping:        [],
		Op.Pong:        [],

		# Bootstrapping:
		Op.GetAcceptedFrontier: [Field.ChainID, Field.RequestID, Field.Deadline],
		Op.AcceptedFrontier:    [Field.ChainID, Field.RequestID, Field.ContainerIDs],
		Op.GetAccepted:         [Field.ChainID, Field.RequestID, Field.Deadline, Field.ContainerIDs],
		Op.Accepted:            [Field.ChainID, Field.RequestID, Field.ContainerIDs],
		Op.GetAncestors:        [Field.ChainID, Field.RequestID, Field.Deadline, Field.ContainerID],
		Op.MultiPut:            [Field.ChainID, Field.RequestID, Field.MultiContainerBytes],

		# Consensus:
		Op.Get:       [Field.ChainID, Field.RequestID, Field.Deadline, Field.ContainerID],
		Op.Put:       [Field.ChainID, Field.RequestID, Field.ContainerID, Field.ContainerBytes],
		Op.PushQuery: [Field.ChainID, Field.RequestID, Field.Deadline, Field.ContainerID, Field.ContainerBytes],
		Op.PullQuery: [Field.ChainID, Field.RequestID, Field.Deadline, Field.ContainerID],
		Op.Chits:     [Field.ChainID, Field.RequestID, Field.ContainerIDs],

		# Signature
		Op.SignedVersion:  [Field.NetworkID, Field.NodeID, Field.MyTime, Field.IP, Field.VersionStr, Field.VersionTime, Field.SigBytes],
		Op.SignedPeerList: [Field.SignedPeers],
	}


	@classmethod
	def get(cls, op):
		if op in cls.__msg_structure:
			return cls.__msg_structure.get(op)

		raise LookupError(f"Message structure not found for Op {op}")            
    