# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avm
import avaxconfig

u, p = avaxconfig.upass()

stt = avm.createAddress(u, p)
print(stt)
