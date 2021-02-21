# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


import avaxpython
import jsrpc
import warnings

caller = avaxpython.get_caller()

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