# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import platform
import sys

subnetID = None
if len(sys.argv) > 1:
    subnetID = sys.argv[1]

stt = platform.getPendingValidators(subnetID)
print(stt)
