# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avm
import sys

address = sys.argv[1]

stt = avm.getAllBalances(address)
print(stt)
