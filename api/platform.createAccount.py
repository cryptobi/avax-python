# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import avaxconfig
import platform

username, password = avaxconfig.upass()

stt = platform.createAccount(username, password)
print(stt)

