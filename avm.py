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


