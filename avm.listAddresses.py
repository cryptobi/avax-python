# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avm
import avaconfig

u, p = avaconfig.upass()

stt = avm.listAddresses(u, p)
print(stt)
