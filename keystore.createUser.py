# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaconfig
import keystore

username, password = avaconfig.upass()

stt = keystore.createUser(username, password)
print(stt)

