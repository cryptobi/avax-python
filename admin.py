# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def getNodeID():

    data = {}

    ret = jsrpc.ava_call(avaconfig.aurl, "admin.getNodeID", data)
    return ret["nodeID"]


def peers():

    data = {}

    ret = jsrpc.ava_call(avaconfig.aurl, "admin.peers", data)
    return ret["peers"]
