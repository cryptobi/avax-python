# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def getLiveness():

    data = {}

    ret = jsrpc.ava_call(avaconfig.hurl, "health.getLiveness", data)
    return ret

