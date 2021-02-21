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


import platform
import admin
import avaxconfig
import time

username, password = avaxconfig.upass()
host_id = admin.getNodeID()
accounts = platform.listAccounts(username, password)
account = accounts[0]

address = account["address"]
nonce = int(account["nonce"])
balance = account["balance"]

minutes_delay = 2
one_day = 24 * 60 * 60
days_stake = 30
stake_seconds = days_stake * one_day

start_time = int(time.time()) + (minutes_delay * 60)
end_time = int(time.time()) + stake_seconds

print("HOST {} ADDRESS {} NONCE {} BALANCE {} START {} END {}".format(host_id, address, nonce,
                                                                      balance, start_time, end_time))

ret = platform.addDefaultSubnetValidator(host_id, nonce+1, address, start_time, end_time, 10000)

utx = ret["unsignedTx"]

sret = platform.sign(utx, address, username, password)

stx = sret["tx"]

iret = platform.issueTx(stx)

print(iret)

