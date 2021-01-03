# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avapython
import jsrpc

caller = avapython.get_caller()

def getBlockchainID(alias):
    
    data = {
        "alias": alias
    }

    ret = caller("info.getBlockchainID", data)
    return ret["blockchainID"]


def getNetworkID():
    
    data = {}

    ret = caller("info.getNetworkID", data)
    return ret["networkID"]


def getNetworkName():
    
    data = {}

    ret = caller("info.getNetworkName", data)
    return ret["networkName"]    


def getNodeID():
    
    data = {}

    ret = caller("info.getNodeID", data)
    return ret["nodeID"]      


def getNodeVersion():
    
    data = {}

    ret = caller("info.getNodeVersion", data)
    return ret["version"]        


def peers():
    
    data = {}

    ret = caller("info.peers", data)
    return ret["peers"]    