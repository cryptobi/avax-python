# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import platform
import sys

subnetID = None
if len(sys.argv) > 1:
    subnetID = sys.argv[1]

stt = platform.getCurrentValidators(subnetID)
print(stt)
