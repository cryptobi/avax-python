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

from avaxpython.ids.ID import ID
from avaxpython.vms import platformvm, avm, evm, timestampvm, secp256k1fx, nftfx, propertyfx
from avaxpython.utils.constants import network_ids
from avaxpython.vms.platformvm.static_service import Genesis
from avaxpython.vms.platformvm import codec

def Aliases(genesisBytes: bytes):
	"""Aliases returns the default aliases based on the network ID"""
	generalAliases = {
		"vm/" + str(platformvm.ID):             ["vm/platform"],
		"vm/" + str(avm.ID):                    ["vm/avm"],
		"vm/" + str(evm.ID):                    ["vm/evm"],
		"vm/" + str(timestampvm.ID):            ["vm/timestamp"],
		"bc/" + str(network_ids.PlatformChainID): ["P", "platform", "bc/P", "bc/platform"],
	}

	chainAliases = {
		str(network_ids.PlatformChainID): ["P", "platform"],
	}

	vmAliases = {
		platformvm.ID:  {"platform"},
		avm.ID:         {"avm"},
		evm.ID:         {"evm"},
		timestampvm.ID: {"timestamp"},
		secp256k1fx.ID: {"secp256k1fx"},
		nftfx.ID:       {"nftfx"},
		propertyfx.ID:  {"propertyfx"},
	}

	genesis = Genesis([], [], [], 0, 0, "")
	#codec.GenesisCodec.Unmarshal(genesisBytes, genesis)
	#genesis.Initialize()

	for _, chain in genesis.Chains:
		uChain = platformvm.UnsignedCreateChainTx(chain.UnsignedTx)
		if uChain.VMID == avm.ID:
			generalAliases["bc/"+chain.ID()] = ["X", "avm", "bc/X", "bc/avm"]
			chainAliases[chain.ID()] = ["X", "avm"]
		elif uChain.VMID == evm.ID:
			generalAliases["bc/"+chain.ID()] = ["C", "evm", "bc/C", "bc/evm"]
			chainAliases[chain.ID()] = ["C", "evm"]
		elif uChain.VMID == timestampvm.ID:
			generalAliases["bc/"+chain.ID()] = ["bc/timestamp"]
			chainAliases[chain.ID()] = ["timestamp"]
		
	
	return generalAliases, chainAliases, vmAliases

