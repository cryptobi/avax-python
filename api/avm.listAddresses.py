# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import avm
import avaxconfig

u, p = avaxconfig.upass()

stt = avm.listAddresses(u, p)
print(stt)
