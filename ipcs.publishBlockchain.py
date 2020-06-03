# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import ipc
import sys

blockchainID = sys.argv[1]

stt = ipc.publishBlockchain(blockchainID)
print(stt)
