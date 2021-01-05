# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

# Publish all blockchains' IPC

import socket
import sys
import platform
import ipcs

blockchains = platform.getBlockchains()

for bc in blockchains["blockchains"]:

    ret = ipcs.publishBlockchain(bc["id"])
    print(ret)
