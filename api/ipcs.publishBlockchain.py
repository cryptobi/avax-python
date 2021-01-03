# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import ipcs
import sys

blockchainID = sys.argv[1]

stt = ipcs.publishBlockchain(blockchainID)
print(stt)
