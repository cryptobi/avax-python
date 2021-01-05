# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import platform
import sys

subnetID = sys.argv[1]

stt = platform.validates(subnetID)
print(stt)
