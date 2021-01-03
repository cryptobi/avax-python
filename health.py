# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avapython
import jsrpc

caller = avapython.get_caller()

def getLiveness():

    data = {}

    ret = caller("health.getLiveness", data)
    return ret

