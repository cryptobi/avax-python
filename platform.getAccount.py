# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaconfig
import avm
import platform
import sys
import time

to_addr = sys.argv[1]

stt = platform.getAccount(to_addr)
print(stt)
init_balance = stt["balance"]
print("BALANCE {}".format(init_balance))
