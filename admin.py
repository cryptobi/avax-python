# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avapython
import jsrpc
import warnings

caller = avapython.get_caller()

def getNodeID():

    warnings.warn("This method is deprecated and will be removed in future versions. Use info.getNodeID instead.", DeprecationWarning)

    data = {}

    ret = caller("admin.getNodeID", data)
    return ret["nodeID"]


def peers():

    warnings.warn("This method is deprecated and will be removed in future versions. Use info.peers instead.", DeprecationWarning)

    data = {}

    ret = caller("admin.peers", data)
    return ret["peers"]


def getNetworkID():

    warnings.warn("This method is deprecated and will be removed in future versions. Use info.getNetworkID instead.", DeprecationWarning)

    data = {}

    ret = caller("admin.getNetworkID", data)
    return ret["networkID"]


def alias(endpoint, alias):

    data = {
        "alias": alias,
        "endpoint": endpoint
    }

    ret = caller("admin.alias", data)
    return ret["success"]


def aliasChain(chain, alias):

    data = {
        "alias": alias,
        "chain": chain
    }

    ret = caller("admin.aliasChain", data)
    return ret["success"]


def getBlockchainID(alias):

    warnings.warn("This method is deprecated and will be removed in future versions. Use info API instead.", DeprecationWarning)

    data = {
        "alias": alias
    }

    ret = caller("admin.getBlockchainID", data)
    return ret["blockchainID"]


def startCPUProfiler(fileName):

    data = {
        "fileName": fileName
    }

    ret = caller("admin.startCPUProfiler", data)
    return ret["success"]


def stopCPUProfiler():

    data = {}

    ret = caller("admin.stopCPUProfiler", data)
    return ret["success"]


def memoryProfile(fileName):

    data = {
        "fileName": fileName
    }

    ret = caller("admin.memoryProfile", data)
    return ret["success"]


def lockProfile(fileName):

    data = {
        "fileName": fileName
    }

    ret = caller("admin.lockProfile", data)
    return ret["success"]