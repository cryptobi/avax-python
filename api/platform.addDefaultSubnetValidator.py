# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

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

