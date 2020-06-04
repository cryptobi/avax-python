# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


# See Ethereum API for reference
# example method https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getbalance
def eth_getBalance(data, quantity_tag):

    args = [data, quantity_tag]

    return jsrpc.ava_call(avaconfig.eurl, "eth_getBalance", args)
