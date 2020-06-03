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

