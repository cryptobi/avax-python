# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaconfig
import platform

username, password = avaconfig.upass()

stt = platform.listAccounts(username, password)
print(stt)
