# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaxpython
import jsrpc

caller = avaxpython.get_caller()

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