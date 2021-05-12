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

from avaxpython.vms.avm.base_tx import BaseTx
from avaxpython.vms.avm.create_asset_tx import CreateAssetTx
from avaxpython.vms.avm.operation_tx import OperationTx
from avaxpython.vms.avm.import_tx import ImportTx
from avaxpython.vms.avm.export_tx import ExportTx
from avaxpython.vms.secp256k1fx.transfer_input import TransferInput
from avaxpython.vms.secp256k1fx.mint_output import MintOutput
from avaxpython.vms.secp256k1fx.transfer_output import TransferOutput
from avaxpython.vms.secp256k1fx.mint_operation import MintOperation
from avaxpython.vms.secp256k1fx.credential import Credential

registered_types = {}
registered_types[0] = BaseTx
registered_types[1] = CreateAssetTx
registered_types[2] = OperationTx
registered_types[3] = ImportTx
registered_types[4] = ExportTx
registered_types[5] = TransferInput
registered_types[6] = MintOutput
registered_types[7] = TransferOutput
registered_types[8] = MintOperation
registered_types[9] = Credential

