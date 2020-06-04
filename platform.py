# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def getAccount(address):
    data = {
        "address": address
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.getAccount", data)


def getSubnets():
    data = {}

    return jsrpc.ava_call(avaconfig.purl, "platform.getSubnets", data)


def createBlockchain(subnetID, vmID, name, payerNonce, genesisData):

    data = {
        "subnetID": subnetID,
        "vmID": vmID,
        "name": name,
        "payerNonce": payerNonce,
        "genesisData": genesisData
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.createBlockchain", data)


def getBlockchainStatus(blockchainID):

    data = {
        "blockchainID": blockchainID
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.getBlockchainStatus", data)



def importAVA(to_addr, nonce, usern, passw):

    data = {
        "to": to_addr,
        "username": usern,
        "password": passw,
        "payerNonce": nonce
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.importAVA", data)


def exportAVA(amount, to, payerNonce):

    data = {
        "amount": amount,
        "to": to,
        "payerNonce": payerNonce
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.importAVA", data)


def issueTx(tx):

    data = {
        "tx": tx
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.issueTx", data)


def listAccounts(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    ret = jsrpc.ava_call(avaconfig.purl, "platform.listAccounts", data)
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

    return jsrpc.ava_call(avaconfig.purl, "platform.addDefaultSubnetValidator", data)


def addNonDefaultSubnetValidator(host_id, subnetID, startTime, endTime, weight, payerNonce):

    data = {
        "id": host_id,
        "subnetID": subnetID,
        "startTime": startTime,
        "endTime": endTime,
        "weight": int(weight),
        "payerNonce": payerNonce
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.addDefaultSubnetValidator", data)


def sign(tx, signer_addr, usern, passw):

    data = {
        "tx": tx,
        "signer": signer_addr,
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.sign", data)


def getPendingValidators(subnetID=None):

    data = {}

    if subnetID:
        data["subnetID"] = subnetID

    return jsrpc.ava_call(avaconfig.purl, "platform.getPendingValidators", data)


def getCurrentValidators(subnetID=None):

    data = {}

    if subnetID:
        data["subnetID"] = subnetID

    return jsrpc.ava_call(avaconfig.purl, "platform.getCurrentValidators", data)


def sampleValidators(subnetID=None, size=50):

    data = {
        "subnetID": subnetID,
        "size": size
    }

    if subnetID:
        data["subnetID"] = subnetID

    return jsrpc.ava_call(avaconfig.purl, "platform.sampleValidators", data)


def validates(subnetID):

    data = {"subnetID": subnetID}

    return jsrpc.ava_call(avaconfig.purl, "platform.validates", data)


def getBlockchains():

    data = {}


    return jsrpc.ava_call(avaconfig.purl, "platform.getBlockchains", data)


def createAccount(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.createAccount", data)


def createSubnet(controlKeys, threshold, payerNonce):

    data = {
        "controlKeys": controlKeys,
        "payerNonce": payerNonce,
        "threshold": threshold
    }

    return jsrpc.ava_call(avaconfig.purl, "platform.createSubnet", data)


