# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import platform

username, password = avaconfig.upass()

stt = platform.listAccounts(username, password)
print(stt)
