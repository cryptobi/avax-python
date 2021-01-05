# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import avaxpython
import jsrpc

caller = avaxpython.get_caller()

def getLiveness():

    data = {}

    ret = caller("health.getLiveness", data)
    return ret

