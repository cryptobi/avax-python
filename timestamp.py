# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def getBlock(block_id):

    params = {
        "id": block_id
    }

    return jsrpc.ava_call(avaconfig.turl, "timestamp.getBlock", params)


def proposeBlock(data):

    params = {
        "data": data
    }

    return jsrpc.ava_call(avaconfig.turl, "timestamp.proposeBlock", params)