# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def getBlockchainID(alias):
    
    data = {
        "alias": alias
    }

    ret = jsrpc.ava_call(avaconfig.iurl, "info.getBlockchainID", data)
    return ret["blockchainID"]


def getNetworkID():
    
    data = {}

    ret = jsrpc.ava_call(avaconfig.iurl, "info.getNetworkID", data)
    return ret["networkID"]


def getNetworkName():
    
    data = {}

    ret = jsrpc.ava_call(avaconfig.iurl, "info.getNetworkName", data)
    return ret["networkName"]    


def getNodeID():
    
    data = {}

    ret = jsrpc.ava_call(avaconfig.iurl, "info.getNodeID", data)
    return ret["nodeID"]      


def getNodeVersion():
    
    data = {}

    ret = jsrpc.ava_call(avaconfig.iurl, "info.getNodeVersion", data)
    return ret["version"]        


def peers():
    
    data = {}

    ret = jsrpc.ava_call(avaconfig.iurl, "info.peers", data)
    return ret["peers"]    