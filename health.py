# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avapython
import jsrpc

caller = avapython.get_caller()

def getLiveness():

    data = {}

    ret = caller("health.getLiveness", data)
    return ret

