# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaxpython
import jsrpc

caller = avaxpython.get_caller()

def getLiveness():

    data = {}

    ret = caller("health.getLiveness", data)
    return ret

