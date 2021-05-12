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

from typing import List
from avaxpython.vms.components.verify.verification import Verifiable
from avaxpython.ids.ID import ID
from avaxpython.types import *
from avaxpython.structured import AvaxStructured

# maxNumParents is the max number of parents a vertex may have
maxNumParents = 128

# maxTxsPerVtx is the max number of transactions a vertex may have
maxTxsPerVtx = 128

errBadVersion          = Exception("invalid version")
errBadEpoch            = Exception("invalid epoch")
errFutureField         = Exception("field specified in a previous version")
errTooManyparentIDs    = f"vertex contains more than {maxNumParents} parentIDs"
errNoOperations        = Exception("vertex contains no operations")
errTooManyTxs          = f"vertex contains more than {maxTxsPerVtx} transactions"
errTooManyRestrictions = f"vertex contains more than {maxTxsPerVtx} restrictions"
errInvalidParents      = Exception("vertex contains non-sorted or duplicated parentIDs")
errInvalidRestrictions = Exception("vertex contains non-sorted or duplicated restrictions")
errInvalidTxs          = Exception("vertex contains non-sorted or duplicated transactions")

class StatelessVertex(Verifiable):

	def __init__(self) -> None:
		Verifiable.__init__(self)

	def ID(self) -> ID:
		pass

	def Bytes(self) -> Bytes:
		pass

	def Version(self) -> int:
		pass

	def ChainID(self) -> ID:
		pass

	def Height(self) -> int:
		pass

	def Epoch(self) -> int:
		pass

	def ParentIDs(self) -> List[ID]:
		pass

	def Txs(self) -> Bytes:
		pass

	def Restrictions(self) -> List[ID]:
		pass


class innerStatelessVertex(AvaxStructured):
	"""A DAG vertex implementation."""

	_avax_tags = [
		("Version", { "json": "version" }),
		("ChainID", { "serialize": True, "json" : "chainID" }),
		("Height", { "serialize": True, "json":"height"}),
		("Epoch", { "serialize": True, "json":"epoch"}),
		("ParentIDs", { "element_type": ID, "serialize": True, "len":"128", "json":"parentIDs"}),
		("Txs", { "element_type": bytes, "serialize": True, "len":"128", "json":"txs"}),
		("Restrictions", { "element_type": ID, "serializeV1": True, "len":"128", "json":"restrictions"}),
	]

	def __init__(self) -> None:		
		self.Version: int = Uint16(0)
		self.ChainID: ID = ID()
		self.Height: int = Uint64(0)
		self.Epoch: int = Uint32(0)
		self.ParentIDs: List[ID] = Slice()
		self.Txs = ByteSlices()
		self.Restrictions: List[ID] = Slice()

	def __struct__(self):
		_d = {}
		for k, v in self._avax_tags:
			_d[k] = str(getattr(self, k))
		
		_s = {
			'innerStatelessVertex' : _d
		}
		
		return _s

	def __str__(self):
		return str(self.__struct__())

	def Initialize(self, Version: Uint16, ChainID: ID, Height, Epoch, ParentIDs, Txs, Restrictions) -> None:		
		self.Version: int = Uint16(Version)
		self.ChainID: ID = ChainID
		self.Height: int = Uint64(Height)
		self.Epoch: int = Uint32(Epoch)
		self.ParentIDs: List[ID] = Slice(ParentIDs)
		self.Txs: ByteSlices = ByteSlices(Txs)
		self.Restrictions: List[ID] = Slice(Restrictions)

	def Verify(self):

		if self.Version != 0:
			raise errBadVersion
		elif self.Epoch != 0:
			raise errBadEpoch
		elif len(self.Restrictions) != 0:
			raise errFutureField			
		elif len(self.ParentIDs) > maxNumParents:
			raise errTooManyparentIDs
		elif len(self.Txs)+len(self.Restrictions) == 0:
			raise errNoOperations
		elif len(self.Txs) > maxTxsPerVtx:
			raise errTooManyTxs
		elif len(self.Restrictions) > maxTxsPerVtx:
			raise errTooManyRestrictions
		elif not ids.IsSortedAndUniqueIDs(self.ParentIDs):
			raise errInvalidParents
		elif not ids.IsSortedAndUniqueIDs(self.Restrictions):
			raise errInvalidRestrictions
		elif not IsSortedAndUniqueHashOf(self.Txs):
			raise errInvalidTxs


class statelessVertex(innerStatelessVertex):
	"""This wrapper exists so that the function calls aren't ambiguous"""
	def __init__(self) -> None:
		super().__init__()
		self.innerStatelessVertex = innerStatelessVertex()

	def __struct__(self):
		_s = {
			'StatelessVertex' : {
				'innerStatelessVertex' : self.innerStatelessVertex
			}
		}
		return _s

	def Initialize(self, Version, ChainID, Height, Epoch, ParentIDs, Txs, Restrictions, 
		idx: ID = ID(), bbytes: bytes = Bytes(), innerStatelessVertex = None) -> None:

		super().Initialize(Version, ChainID, Height, Epoch, ParentIDs, Txs, Restrictions)

		# cache the ID of this vertex
		self.id: ID = idx

		# cache the binary format of this vertex
		self.bytes: bytes = bbytes
		self.innerStatelessVertex = innerStatelessVertex

	def ID(self) -> ID:
		return self.id

	def Bytes(self) -> bytes:
		return self.bytes

	def Version(self) -> int:
		return self.Version

	def ChainID(self) -> ID:
		return self.ChainID

	def Height(self) -> int:
		return self.Height

	def Epoch(self) -> int:
		return self.ParentIDs

	def Txs(self):
		return self.Txs
	
	def Restrictions(self):
		return self.Restriction

