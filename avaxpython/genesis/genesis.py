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

from typing import List, Tuple
from avaxpython.ids.ID import ID
from avaxpython.genesis import config as config_pkg
from avaxpython.genesis.config import Config
from avaxpython.utils import constants


def Genesis(networkID: int, filepath: str) -> Tuple[bytes, ID]:
	""" Genesis returns the genesis data of the Platform Chain.

	Since an Avalanche network has exactly one Platform Chain, and the Platform
	Chain defines the genesis state of the network (who is staking, which chains
	exist, etc.), defining the genesis state of the Platform Chain is the same as
	defining the genesis state of the network.

	Genesis accepts:
	1) The ID of the new network. [networkID]
	2) The location of a custom genesis config to load. [filepath]

	If [filepath] is empty or the given network ID is Mainnet, Testnet, or Local, loads the
	network genesis state from predefined configs. If [filepath] is non-empty and networkID
	isn't Mainnet, Testnet, or Local, loads the network genesis data from the config at [filepath].

	Genesis returns:
	1) The byte representation of the genesis state of the platform chain
		(ie the genesis state of the network)
	2) The asset ID of AVAX"""

	config = config_pkg.GetConfig(networkID)

	return FromConfig(config)


def FromConfig(config: Config) -> Tuple[bytes, ID]:
	"""FromConfig returns:
	1) The byte representation of the genesis state of the platform chain (ie the genesis state of the network)
	2) The asset ID of AVAX"""

	ret_b = b""	
	ret_id = ID()
	return ret_b, ret_id
