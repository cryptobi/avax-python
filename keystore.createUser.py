# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import keystore

username, password = avaconfig.upass()

stt = keystore.createUser(username, password)
print(stt)

