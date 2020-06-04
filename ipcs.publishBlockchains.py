# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

# Publish all blockchains' IPC

import socket
import sys
import platform
import ipcs

blockchains = platform.getBlockchains()

for bc in blockchains["blockchains"]:

    ret = ipcs.publishBlockchain(bc["id"])
    print(ret)
