# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaxconfig
import platform

username, password = avaxconfig.upass()

stt = platform.createAccount(username, password)
print(stt)

