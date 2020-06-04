# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def publishBlockchain(blockchainID):

    data = {
        "blockchainID": blockchainID
    }

    return jsrpc.ava_call(avaconfig.iurl, "ipcs.publishBlockchain", data)


def unpublishBlockchain(blockchainID):

    data = {
        "blockchainID": blockchainID
    }

    return jsrpc.ava_call(avaconfig.iurl, "ipcs.unpublishBlockchain", data)
