# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import avaxconfig
import avm
import platform
import sys
import time

to_addr = sys.argv[1]

stt = platform.getAccount(to_addr)
print(stt)
init_balance = stt["balance"]
print("BALANCE {}".format(init_balance))
