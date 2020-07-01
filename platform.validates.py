# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import platform
import sys

subnetID = sys.argv[1]

stt = platform.validates(subnetID)
print(stt)
