# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

# Publish all blockchains' IPC

import socket
import sys
import platform
import ipc

blockchains = platform.getBlockchains()

for bc in blockchains["blockchains"]:

    ret = ipc.publishBlockchain(bc["id"])
    print(ret)
