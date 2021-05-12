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
from avaxpython.ids.ID import ID
from avaxpython.vms.avm.tx import Tx as AvmTx, UnsignedTx
from avaxpython.snow.choices.status import Status
from avaxpython.vms.components.avax.utxo import UTXO
from avaxpython.vms.components.avax.utxo_id import UTXOID
from avaxpython.snow.consensus.snowstorm.tx import Tx as SnowstormTx
from avaxpython.utils.formatting.encoding import Encoding

errAssetIDMismatch = Exception("asset IDs in the input don't match the utxo")
errWrongAssetID    = Exception("asset ID must be AVAX in the atomic tx")
errMissingUTXO     = Exception("missing utxo")
errUnknownTx       = Exception("transaction is unknown")
errRejectedTx      = Exception("transaction is rejected")

class TxState(AvmTx):
	def __init__(self, Tx=None, vm=None, txID=None, unique=None, verifiedTx=None, verifiedState=None, validity=None, inputs=None, inputUTXOs=None, utxos=None, deps=None, status: Status=None):
		self.Tx = Tx
		self.unique = unique
		self.verifiedTx = verifiedTx
		self.verifiedState = verifiedState
		self.validity = validity
		self.inputs: List[ID] = inputs
		self.inputUTXOs: List[UTXOID] = inputUTXOs
		self.utxos: List[UTXO] = utxos
		self.deps: List[SnowstormTx] = deps
		self.status: Status = status

	def __struct__(self):
		_s_d = {
			'unique' : self.unique,
			'verifiedTx' : self.verifiedTx,
			'validity' : self.validity,
			'inputs' : self.inputs,
			'inputUTXOs' : self.inputUTXOs,
			'utxos': self.utxos,
			'deps' : self.deps,
			'status' : self.status,
			'Tx' : {
				'UnsignedTx' : self.Tx.UnsignedTx,
				'Creds' : self.Tx.Creds
			}
		}
		_s = {
			'TxState' : _s_d
		}

		return _s


class UniqueTx(TxState):
	"""UniqueTx provides a de-duplication service for txs. This only provides a performance boost"""
	def __init__(self, vm, txID, TxState=None):
		self.vm = vm
		self.txID: ID = txID
		self.TxState = TxState

	def SyntacticVerify(self):
    		return True

	def __struct__(self):
		enc = Encoding()
		_s = {
			'UniqueTx' : {
				'txID' : enc.Encode(self.txID),
				'state' : self.TxState
			}
		}
		return _s
