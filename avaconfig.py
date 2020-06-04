# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

jsonrpc_host = "127.0.0.1"
jsonrpc_port = "9650"
jsonrpc_prot = "http"
jsonrpc_url = "{}://{}:{}".format(jsonrpc_prot, jsonrpc_host, jsonrpc_port)

xurl = "{}/ext/bc/X".format(jsonrpc_url)  # x-chain url
purl = "{}/ext/bc/P".format(jsonrpc_url)  # p-chain url
kurl = "{}/ext/keystore".format(jsonrpc_url)  # keystore url
aurl = "{}/ext/admin".format(jsonrpc_url)  # admin url
iurl = "{}/ext/ipcs".format(jsonrpc_url)  # ipcs url
hurl = "{}/ext/health".format(jsonrpc_url)  # health url


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

