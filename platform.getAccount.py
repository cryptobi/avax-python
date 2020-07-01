# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
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
