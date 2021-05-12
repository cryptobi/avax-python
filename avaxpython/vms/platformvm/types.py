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

from avaxpython.vms.secp256k1fx.output_owners import OutputOwners
from avaxpython.vms.secp256k1fx.input import Input
from avaxpython.vms.secp256k1fx.transfer_input import TransferInput
from avaxpython.vms.secp256k1fx.mint_output import MintOutput
from avaxpython.vms.secp256k1fx.transfer_output import TransferOutput
from avaxpython.vms.secp256k1fx.mint_operation import MintOperation
from avaxpython.vms.secp256k1fx.credential import Credential
from avaxpython.vms.platformvm.proposal_block import ProposalBlock
from avaxpython.vms.platformvm.commit_block import Commit
from avaxpython.vms.platformvm.abort_block import Abort
from avaxpython.vms.platformvm.standard_block import StandardBlock
from avaxpython.vms.platformvm.atomic_block import AtomicBlock
from avaxpython.vms.platformvm.add_validator_tx import UnsignedAddValidatorTx
from avaxpython.vms.platformvm.add_subnet_validator_tx import UnsignedAddSubnetValidatorTx
from avaxpython.vms.platformvm.add_delegator_tx import UnsignedAddDelegatorTx
from avaxpython.vms.platformvm.create_chain_tx import UnsignedCreateChainTx
from avaxpython.vms.platformvm.create_subnet_tx import UnsignedCreateSubnetTx
from avaxpython.vms.platformvm.import_tx import UnsignedImportTx
from avaxpython.vms.platformvm.export_tx import UnsignedExportTx
from avaxpython.vms.platformvm.advance_time_tx import UnsignedAdvanceTimeTx
from avaxpython.vms.platformvm.reward_validator_tx import UnsignedRewardValidatorTx
from avaxpython.vms.platformvm.stakeable_lock import StakeableLockIn, StakeableLockOut

registered_types = {}
registered_types[0] = ProposalBlock
registered_types[1] = Abort
registered_types[2] = Commit
registered_types[3] = StandardBlock
registered_types[4] = AtomicBlock
registered_types[5] = TransferInput
registered_types[6] = MintOutput
registered_types[7] = TransferOutput
registered_types[8] = MintOperation
registered_types[9] = Credential
registered_types[10] = Input
registered_types[11] = OutputOwners
registered_types[12] = UnsignedAddValidatorTx
registered_types[13] = UnsignedAddSubnetValidatorTx
registered_types[14] = UnsignedAddDelegatorTx
registered_types[15] = UnsignedCreateChainTx
registered_types[16] = UnsignedCreateSubnetTx
registered_types[17] = UnsignedImportTx
registered_types[18] = UnsignedExportTx
registered_types[19] = UnsignedAdvanceTimeTx
registered_types[20] = UnsignedRewardValidatorTx
registered_types[21] = StakeableLockIn
registered_types[22] = StakeableLockOut