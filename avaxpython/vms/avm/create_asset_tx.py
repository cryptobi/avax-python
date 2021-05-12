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

from avaxpython.types import Byte, Slice
from avaxpython.vms.avm.base_tx import BaseTx
from avaxpython.vms.avm.initial_state import InitialState
from avaxpython.structured import AvaxStructured

class CreateAssetTx(BaseTx, AvaxStructured):
	_avax_tags = [
		("BaseTx", { "serialize": True}),
		("Name", { "serialize": True, "json" : "name" }),
		("Symbol", { "serialize": True, "json":"symbol"}),
		("Denomination", {"serialize": True, "json":"denomination"}),
		("States", { "element_type": InitialState, "serialize": True, "json":"initialStates"}),
	]

	def __init__(self):
		BaseTx.__init__(self)
		self.BaseTx = BaseTx()
		self.Name = str()
		self.Symbol = str()
		self.Denomination = Byte()
		self.States = Slice()


	# InitialStates track which virtual machines, and the initial state of these
	# machines, this asset uses. The returned array should not be modified.
	def InitialStates(self):
    		return self.States

	# UTXOs returns the UTXOs transaction is producing.
	def UTXOs(self):
		txID = self.ID()
		utxos = self.BaseTx.UTXOs()

		for state in self.States:
			for out in state.Outs:
				utxos.append(avax.UTXO(
					UTXOID = UTXOID(
						TxID = txID,
						OutputIndex = len(utxos),
					),
					Asset = Asset(
						ID = txID,
					),
					Out = out,
				))

		return utxos

	
	def SyntacticVerify(self, ctx, c, txFeeAssetID, a, txFee, numFxs):
		"""SyntacticVerify that this transaction is well-formed."""		


	def Sort(self):
		pass
