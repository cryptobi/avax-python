# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avm
import avaconfig

u, p = avaconfig.upass()

stt = avm.listAddresses(u, p)
print(stt)
