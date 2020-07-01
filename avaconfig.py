# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

from apimeta import api_endpoints

jsonrpc_host = "127.0.0.1"
jsonrpc_port = "9650"
jsonrpc_prot = "http"
jsonrpc_url = "{}://{}:{}".format(jsonrpc_prot, jsonrpc_host, jsonrpc_port)

urls = {k: ("{}" + v).format(jsonrpc_url) for k, v in api_endpoints.items()}

def load_upass():
    rk = {}
    with open("userpass.txt", "r") as f:
        lin = f.readline().strip()
        while lin:
            k, v = lin.split('=')
            rk[k] = v
            lin = f.readline()
    return rk


def upass():
    """Returns user pass as tuple."""
    upass = load_upass()
    username = upass['avmusername']
    password = upass['avmpassword']
    return username, password

