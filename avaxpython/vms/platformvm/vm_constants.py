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
from avaxpython.types import Uint64
from avaxpython.utils.units.avax import MegaAvax

validatorsTypeID = Uint64(0)
chainsTypeID = Uint64(1)

# 2 unused
subnetsTypeID  = Uint64(3)
utxoTypeID = Uint64(4)

# 5 unused
txTypeID = Uint64(6)
statusTypeID = Uint64(7)
currentSupplyTypeID = Uint64(8)

# PercentDenominator is the denominator used to calculate percentages
PercentDenominator = 1000000
droppedTxCacheSize = 50
maxUTXOsToFetch = 1024

# MaxSubMinConsumptionRate is the % consumption that incentivizes staking longer
MaxSubMinConsumptionRate = 20000 # 2%

# MinConsumptionRate is the minimum % consumption of the remaining tokens to be minted
MinConsumptionRate = 100000 # 10%

# SupplyCap is the maximum amount of AVAX that should ever exist
SupplyCap = 720 * MegaAvax

# Maximum future start time for staking/delegating
maxFutureStartTime = 24 * 7 * 2 * (60 * 60)
