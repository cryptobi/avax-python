# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avm
import sys

address = sys.argv[1]

stt = avm.getAllBalances(address)
print(stt)
