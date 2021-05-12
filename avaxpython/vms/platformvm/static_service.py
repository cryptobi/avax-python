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
from avaxpython import ids
from avaxpython.ids import ToShortID
from avaxpython.vms.components.avax.utxo import UTXO
from avaxpython.vms.components.avax.asset import Asset as AvaxAsset
from avaxpython.vms.components.avax.utxo_id import UTXOID
from avaxpython.utils.formatting.addresses import ParseBech32
from avaxpython.vms.platformvm.tx import Tx

# Note that since an Avalanche network has exactly one Platform Chain,
# and the Platform Chain defines the genesis state of the network
# (who is staking, which chains exist, etc.), defining the genesis
# state of the Platform Chain is the same as defining the genesis
# state of the network.


errUTXOHasNoValue       = Exception("genesis UTXO has no value")
errValidatorAddsNoValue = Exception("validator would have already unstaked")
errStakeOverflow        = Exception("too many funds staked on single validator")


class APIUTXO:
    """APIUTXO is a UTXO on the Platform Chain that exists at the chain's genesis."""
    def __init__(self, locktime, amount, addr, msg) -> None:        
        self.Locktime : int = locktime
        self.Amount : int = amount
        self.Address : str = addr
        self.Message : str = msg


class APIStaker:
    """APIStaker is the representation of a staker sent via APIs.
        [TxID] is the txID of the transaction that added this staker.
        [Amount] is the amount of tokens being staked.
        [StartTime] is the Unix time when they start staking
        [Endtime] is the Unix time repr. of when they are done staking
        [NodeID] is the node ID of the staker
        """
    def __init__(self, txid: ID, start_time, end_time, weight, stake_amount, node_id: str) -> None:                
        self.TxID : ID = txid
        self.StartTime: int = start_time
        self.EndTime: int = end_time
        self.Weight: int = weight
        self.StakeAmount : int = stake_amount
        self.NodeID: str = node_id

    def weight(self) -> int:
        if self.Weight != None:
            return int(self.Weight)
        elif self.StakeAmount != None:
            return int(self.StakeAmount)
        else:
            return 0


class APIOwner:
    """APIOwner is the repr. of a reward owner sent over APIs."""
    def __init__(self, locktime: int, threshold: int, addresses: List[str]) -> None:
        self.Locktime = locktime
        self.Threshold = threshold
        self.Addresses = addresses


class APIPrimaryDelegator(APIStaker):
    """APIPrimaryDelegator is the repr. of a primary network delegator sent over APIs."""
    def __init__(self, txid: ID, start_time, end_time, weight, stake_amount, node_id: str, reward_owner: APIOwner, potential_reward: int) -> None:
        super().__init__(txid, start_time, end_time, weight, stake_amount, node_id)

        self.RewardOwner = reward_owner
        self.PotentialReward = potential_reward



class APIPrimaryValidator(APIStaker):
	"""APIPrimaryValidator is the repr. of a primary network validator sent over APIs."""	
	def __init__(self, txid: ID, start_time, end_time, weight, stake_amount, node_id: str, reward_owner: APIOwner, potential_reward: int, delegation_fee: float, exact_delegation_fee:int, uptime, connected, staked, delegators: List[APIPrimaryDelegator]) -> None:
		super().__init__(txid, start_time, end_time, weight, stake_amount, node_id)
		# The owner the staking reward, if applicable, will go to
		self.RewardOwner: APIOwner = reward_owner
		self.PotentialReward = potential_reward
		self.DelegationFee = delegation_fee
		self.ExactDelegationFee = exact_delegation_fee
		self.Uptime = uptime
		self.Connected = connected
		self.Staked = staked
		# The delegators delegating to this validator
		self.Delegators = delegators



class APIChain:
	"""APIChain defines a chain that exists
		at the network's genesis.
		[GenesisData] is the initial state of the chain.
		[VMID] is the ID of the VM this chain runs.
		[FxIDs] are the IDs of the Fxs the chain supports.
		[Name] is a human-readable, non-unique name for the chain.
		[SubnetID] is the ID of the subnet that validates the chain"""
	def __init__(self, genesis_data:str, vmid:ID, fxids:List[ID], name:str, subnet_id: ID) -> None:        
		self.GenesisData = genesis_data
		self.VMID = vmid
		self.FxIDs = fxids
		self.Name = name
		self.SubnetID=subnet_id



class BuildGenesisArgs:
	"""BuildGenesisArgs are the arguments used to create
		the genesis data of the Platform Chain.
		[NetworkID] is the ID of the network
		[UTXOs] are the UTXOs on the Platform Chain that exist at genesis.
		[Validators] are the validators of the primary network at genesis.
		[Chains] are the chains that exist at genesis.
		[Time] is the Platform Chain's time at network genesis."""
	def __init__(self, avax_asset_id, network_id, utxos, validators, chains, a_time, initial_supply, message, encoding) -> None:				
		self.AvaxAssetID = avax_asset_id
		self.NetworkID = network_id
		self.UTXOs = utxos
		self.Validators = validators
		self.Chains = chains
		self.Time = a_time
		self.InitialSupply = initial_supply
		self.Message = message
		self.Encoding = encoding


# BuildGenesisReply is the reply from BuildGenesis
class BuildGenesisReply:
	def __init__(self, bbytes, a_encoding) -> None:		
		self.Bytes = bbytes
		self.Encoding = a_encoding


# GenesisUTXO adds messages to UTXOs
class GenesisUTXO(UTXO):
	def __init__(self, msg) -> None:		
		UTXO.__init__(self)
		self.Message = msg


# Genesis represents a genesis state of the platform chain
class Genesis:
	def __init__(self, utxos: List[GenesisUTXO], validators: List[Tx], chains: List[Tx], timestamp: int, initial_supply: int, message: str) -> None:
		self.UTXOs = utxos
		self.Validators = validators
		self.Chains = chains
		self.Timestamp = timestamp
		self.InitialSupply = initial_supply
		self.Message = message

	def Initialize(self):
		for tx in self.Validators:
			tx.Sign(GenesisCodec, None)
					
		for tx in self.Chains:
			tx.Sign(GenesisCodec, nil)
					
		

# beck32ToID takes bech32 address and produces a shortID
def bech32ToID(address: str):
	_ , addr = ParseBech32(address)
	
	return ToShortID(addr)

class StaticService:
    """StaticService defines the static API methods exposed by the platform VM"""
    pass


def BuildGenesis(ss, http_req, args: BuildGenesisArgs, reply: BuildGenesisReply):
	"""BuildGenesis build the genesis state of the Platform Chain (and thereby the Avalanche network.)"""	

	# genesis holds the genesis state
	return Genesis([], [], [], 0, 0, "")

	

def CreateStaticService() -> StaticService:
	return StaticService()
