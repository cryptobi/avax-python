# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import ipcs
import sys

blockchainID = sys.argv[1]

stt = ipcs.publishBlockchain(blockchainID)
print(stt)
