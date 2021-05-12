# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Support this Open Source project!
Donate to X-avax1qr6yzjykcjmeflztsgv6y88dl0xnlel3chs3r4

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


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

