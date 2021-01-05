# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import platform
import sys

subnetID = None
if len(sys.argv) > 1:
    subnetID = sys.argv[1]

stt = platform.getCurrentValidators(subnetID)
print(stt)
