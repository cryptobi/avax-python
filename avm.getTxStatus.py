# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avm
import sys

txid = sys.argv[1]

stt = avm.getTxStatus(txid)
print(stt)
