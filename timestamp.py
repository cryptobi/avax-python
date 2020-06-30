# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avapython
import jsrpc

caller = avapython.get_caller()

def getBlock(block_id):

    params = {
        "id": block_id
    }

    return caller("timestamp.getBlock", params)


def proposeBlock(data):

    params = {
        "data": data
    }

    return caller("timestamp.proposeBlock", params)