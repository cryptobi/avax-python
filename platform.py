# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avapython
import jsrpc

caller = avapython.get_caller()

def getAccount(address):
    data = {
        "address": address
    }

    return caller("platform.getAccount", data)


def getSubnets():
    data = {}

    return caller("platform.getSubnets", data)


def createBlockchain(subnetID, vmID, name, payerNonce, genesisData):

    data = {
        "subnetID": subnetID,
        "vmID": vmID,
        "name": name,
        "payerNonce": payerNonce,
        "genesisData": genesisData
    }

    return caller("platform.createBlockchain", data)


def getBlockchainStatus(blockchainID):

    data = {
        "blockchainID": blockchainID
    }

    return caller("platform.getBlockchainStatus", data)



def importAVA(to_addr, nonce, usern, passw):

    data = {
        "to": to_addr,
        "username": usern,
        "password": passw,
        "payerNonce": nonce
    }

    return caller("platform.importAVA", data)


def exportAVA(amount, to, payerNonce):

    data = {
        "amount": amount,
        "to": to,
        "payerNonce": payerNonce
    }

    return caller("platform.importAVA", data)


def issueTx(tx):

    data = {
        "tx": tx
    }

    return caller("platform.issueTx", data)


def listAccounts(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    ret = caller("platform.listAccounts", data)
    return ret["accounts"]


def addDefaultSubnetValidator(host_id, nonce, dest_addr, start_time, end_time, amount):

    data = {
        "id": host_id,
        "payerNonce": nonce,
        "destination": dest_addr,
        "startTime": start_time,
        "endTime": end_time,
        "stakeAmount": int(amount)
    }

    return caller("platform.addDefaultSubnetValidator", data)


def addNonDefaultSubnetValidator(host_id, subnetID, startTime, endTime, weight, payerNonce):

    data = {
        "id": host_id,
        "subnetID": subnetID,
        "startTime": startTime,
        "endTime": endTime,
        "weight": int(weight),
        "payerNonce": payerNonce
    }

    return caller("platform.addDefaultSubnetValidator", data)


def sign(tx, signer_addr, usern, passw):

    data = {
        "tx": tx,
        "signer": signer_addr,
        "username": usern,
        "password": passw
    }

    return caller("platform.sign", data)


def getPendingValidators(subnetID=None):

    data = {}

    if subnetID:
        data["subnetID"] = subnetID

    return caller("platform.getPendingValidators", data)


def getCurrentValidators(subnetID=None):

    data = {}

    if subnetID:
        data["subnetID"] = subnetID

    return caller("platform.getCurrentValidators", data)


def sampleValidators(subnetID=None, size=50):

    data = {
        "subnetID": subnetID,
        "size": size
    }

    if subnetID:
        data["subnetID"] = subnetID

    return caller("platform.sampleValidators", data)


def validates(subnetID):

    data = {"subnetID": subnetID}

    return caller("platform.validates", data)


def getBlockchains():

    data = {}


    return caller("platform.getBlockchains", data)


def createAccount(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return caller("platform.createAccount", data)


def createSubnet(controlKeys, threshold, payerNonce):

    data = {
        "controlKeys": controlKeys,
        "payerNonce": payerNonce,
        "threshold": threshold
    }

    return caller("platform.createSubnet", data)


