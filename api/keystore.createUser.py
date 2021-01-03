# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaxconfig
import keystore

username, password = avaxconfig.upass()

stt = keystore.createUser(username, password)
print(stt)

