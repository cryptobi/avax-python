# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def exportAVA(to_addr, amt, usern, passw):

    data = {
        "to": to_addr,
        "amount": int(amt),
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.exportAVA", data)


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


def createAddress(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.createAddress", data)


def listAddresses(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.listAddresses", data)


def issueTx(tx):

    data = {
        "tx": tx
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.issueTx", data)


def signMintTx(tx, minter, usern, passw):

    data = {
        "tx": tx,
        "minter": minter,
        "username": usern,
        "password": passw
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



def send(amount, assetID, to, usern, passw):

    data = {
        "amount": amount,
        "assetID": assetID,
        "to": to,
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.send", data)


def createFixedCapAsset(name, symbol, denomination, initialHolders, usern, passw):

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
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.createFixedCapAsset", data)



def createVariableCapAsset(name, symbol, denomination, minterSets, usern, passw):

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
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.xurl, "avm.createVariableCapAsset", data)


