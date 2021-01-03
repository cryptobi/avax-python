# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import platform
import sys

subnetID = None
if len(sys.argv) > 1:
    subnetID = sys.argv[1]

stt = platform.getPendingValidators(subnetID)
print(stt)
