# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avm
import avaconfig

u, p = avaconfig.upass()

stt = avm.createAddress(u, p)
print(stt)
