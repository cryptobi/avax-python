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

from avaxpython.types import Uint64, Uint32, Bytes
from avaxpython.snow.consensus.snowstorm.tx import Tx as SnowstormTx
from avaxpython.snow.choices.decidable import Decidable

class Vertex(Decidable):
	
	_avax_interface = True

	def __init__(self) -> None:
		super().__init__()
		"""Interface"""

	def Parents(self):
		"""Returns the vertices this vertex depends on"""

	def Height(self) -> Uint64:
		"""Returns the height of this vertex. A vertex's height is defined by one
		greater than the maximum height of the parents."""

	def Epoch(self) -> Uint32:
		"""Returns the epoch this vertex was issued in."""

	def Txs(self) -> SnowstormTx:
		"""Returns a series of state transitions to be performed on acceptance"""


	def Bytes(self) -> Bytes:
		"""Returns the binary representation of this vertex"""
