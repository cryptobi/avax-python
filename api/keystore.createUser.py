# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import avaxconfig
import keystore

username, password = avaxconfig.upass()

stt = keystore.createUser(username, password)
print(stt)

