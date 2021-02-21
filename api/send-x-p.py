# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


# send AVA from X to P chain
# usage <dsst_addr> <amnt>

import avaxconfig
import avm
import platform
import sys
import time


if len(sys.argv) != 3:
    print("Usage: python3 {} <dsst_addr> <amnt>".format(sys.argv[0]))
    exit(1)

to_addr = sys.argv[1]
amnt = sys.argv[2]

username, password = avaxconfig.upass()

stt = platform.getAccount(to_addr)
print(stt)
init_balance = stt["balance"]
print("BALANCE {}".format(init_balance))
nonce = int(stt["nonce"])

ave = avm.exportAVA(to_addr, amnt, username, password)
print(ave)
txID = ave["txID"]
tx_confirmed = False

while not tx_confirmed:

    st = avm.getTxStatus(txID)
    print("TX STATUS {}".format(st))
    time.sleep(2)

    if "status" in st:
        st1 = st["status"]

        if st1 == "Rejected":
            print("TX Rejected. Exiting")
            exit(1)

        tx_confirmed = (st1 == "Accepted")

print("importAVA")
avi = platform.importAVA(to_addr, nonce+1, username, password)
print(avi)

tx_hash = avi["tx"]

print("issueTx")
ret = platform.issueTx(tx_hash)
print(ret)

txID = ret["txID"]

print("getAccount")
stt = platform.getAccount(to_addr)
print(stt)
