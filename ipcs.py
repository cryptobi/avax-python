# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avapython
import jsrpc

caller = avapython.get_caller()

def publishBlockchain(blockchainID):

    data = {
        "blockchainID": blockchainID
    }

    return caller("ipcs.publishBlockchain", data)


def unpublishBlockchain(blockchainID):

    data = {
        "blockchainID": blockchainID
    }

    return caller("ipcs.unpublishBlockchain", data)
