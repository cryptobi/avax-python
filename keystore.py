# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc

def listUsers():

    data = {}

    return jsrpc.ava_call(avaconfig.kurl, "keystore.listUsers", data)


def createUser(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.kurl, "keystore.createUser", data)


def deleteUser(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.kurl, "keystore.deleteUser", data)


def exportUser(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return jsrpc.ava_call(avaconfig.kurl, "keystore.exportUser", data)


def importUser(usern, passw, user):

    data = {
        "username": usern,
        "password": passw,
        "user": user
    }

    return jsrpc.ava_call(avaconfig.kurl, "keystore.importUser", data)


