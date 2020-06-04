# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def buildGenesis(genesisData):

    data = {
        "genesisData": genesisData
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.buildGenesis", data)


def importKey(privateKey, username, password):

    data = {
        "privateKey": privateKey,
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.importKey", data)


def exportKey(address, username, password):

    data = {
        "address": address,
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.exportKey", data)


def exportAVA(to_addr, amt, username, password):

    data = {
        "to": to_addr,
        "amount": int(amt),
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.exportAVA", data)


def importAVA(to, username, password):

    data = {
        "to": to,
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.importAVA", data)


def getAllBalances(address):

    data = {
        "address": address
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.getAllBalances", data)


def getBalance(address, assetID):

    data = {
        "address": address,
        "assetID": assetID
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.getBalance", data)


def getUTXOs(addresses):

    data = {
        "addresses": addresses
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.getUTXOs", data)


def getTxStatus(txID):

    data = {
        "txID": txID
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.getTxStatus", data)


def createAddress(username, password):

    data = {
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.createAddress", data)


def listAddresses(username, password):

    data = {
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.listAddresses", data)


def issueTx(tx):

    data = {
        "tx": tx
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.issueTx", data)


def signMintTx(tx, minter, username, password):

    data = {
        "tx": tx,
        "minter": minter,
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.signMintTx", data)


def createMintTx(amount, assetID, to, minters):

    data = {
        "amount": amount,
        "assetID": assetID,
        "to": to,
        "minters": minters
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.createMintTx", data)



def send(amount, assetID, to, username, password):

    data = {
        "amount": amount,
        "assetID": assetID,
        "to": to,
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.send", data)


def createFixedCapAsset(name, symbol, denomination, initialHolders, username, password):

    """
     initialHolders = [{
        address: string,
        amount: int
    }, ...]
    """

    data = {
        "name": name,
        "symbol": symbol,
        "denomination": denomination,
        "initialHolders": initialHolders,
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.createFixedCapAsset", data)



def createVariableCapAsset(name, symbol, denomination, minterSets, username, password):

    """
     minterSets = [{
        minters: [string],
        threshold: int
    }, ...]
    """

    data = {
        "name": name,
        "symbol": symbol,
        "denomination": denomination,
        "minterSets": minterSets,
        "username": username,
        "password": password
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.createVariableCapAsset", data)


def getAssetDescription(assetID):

    data = {
        "assetID": assetID
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.getAssetDescription", data)


