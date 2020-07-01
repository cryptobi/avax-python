# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avapython
import jsrpc

caller = avapython.get_caller()

# See Ethereum API for reference
# example method https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getbalance
def eth_getBalance(data, quantity_tag):

    args = [data, quantity_tag]

    return caller("eth_getBalance", args)
