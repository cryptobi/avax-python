# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import platform
import sys

subnetID = sys.argv[1]

stt = platform.validates(subnetID)
print(stt)
