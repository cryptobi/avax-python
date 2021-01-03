# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

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
