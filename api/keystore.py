# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

import avaxpython
import jsrpc

caller = avaxpython.get_caller()

def listUsers():

    data = {}

    return caller("keystore.listUsers", data)


def createUser(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return caller("keystore.createUser", data)


def deleteUser(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return caller("keystore.deleteUser", data)


def exportUser(usern, passw):

    data = {
        "username": usern,
        "password": passw
    }

    return caller("keystore.exportUser", data)


def importUser(usern, passw, user):

    data = {
        "username": usern,
        "password": passw,
        "user": user
    }

    return caller("keystore.importUser", data)


