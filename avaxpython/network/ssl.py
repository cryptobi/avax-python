
# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


from pathlib import Path
import os.path as op
import socket
import ssl
from avaxpython import Config as AVAXConfig

__context = None


def get_cert_key(avax_config: AVAXConfig):
    """Retrieves a certificate and key file pair for the provided Config object"""
    hdir = str(Path.home())
    cert_file = op.join(hdir, avax_config.get("staker_crt"))
    key_file = op.join(hdir, avax_config.get("staker_key"))

    if not op.isfile(cert_file):
        raise Exception(f"Unable to find certificate file at {cert_file}")

    if not op.isfile(key_file):
        raise Exception(f"Unable to find key file at {key_file}")

    return (cert_file, key_file)


def ssl_connect(hostname, port):
    
    sock = socket.create_connection((hostname, port))
    return context_singleton().wrap_socket(sock, server_hostname=hostname)


def context_singleton(avax_config: AVAXConfig):

    global __context

    if __context == None:
        
        __context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        __context.check_hostname = False
        __context.verify_mode = ssl.CERT_NONE
        __context.load_cert_chain(certfile=avax_config.get("staker_crt"), keyfile=avax_config.get("staker_key"))


    return __context
    