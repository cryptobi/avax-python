#!/usr/bin/python3

# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

# list_peers.py - Recursively fetch AVAX peers until cancelled.

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


import socket
import ssl
import avaxpython
from avaxpython import Config
from avaxpython.Config import Config as AVAXConfig
from avaxpython.genesis import beacons
from avaxpython.utils import constants
from avaxpython.utils.wrappers.Packer import Packer
from avaxpython.network.network import Network
from avaxpython.node.node import Node
from avaxpython.network.Messages import Messages
from avaxpython.network.Field import Field
from avaxpython.network.Op import Op
from avaxpython.network.Msg import Msg
from avaxpython.network.codec import Codec

# Download and build the official AVAX implementation in Go
# cd ~/go/src/github.com/ava-labs/
# git clone https://github.com/ava-labs/avalanchego.git
# cd avalanchego
# 
# Run the Go client once to generate the needed certs
#

# Lib ------------------------------------------------------------------------


def avax_handle_msg(msg):
    logger.debug("avax_handle_msg called with {} bytes".format(len(msg)))
    parsed_msg = Codec.Parse(msg)
    print(parsed_msg)


def avax_handle_protocol(conn):
    """Handle the AVAX protocol using SSL socket conn."""

    while True:

        r = conn.recv(Config.DEFAULT_BUFFIZ)

        if not r:
            logger.error("Nothing received from {}:{} . Aborting connection.".format(host_addr, host_port))
            break

        r_len = len(r)

        if r_len == Packer.IntLen:
            pak_len = int.from_bytes(r, "big")
            logger.debug("Attempting to read {} bytes".format(pak_len))            
            pak = conn.recv(pak_len)
            if len(pak) == pak_len:
                logger.debug("Received {} bytes.".format(pak_len))
                avax_handle_msg(pak)
            else:
                logger.warning("Message size {} and received size {} differ. Message ignored.".format(pak_len, len(pak)))


    logger.debug("Closing connection")
    conn.close()


def avax_dispatch_host(beacon_hp, beacon_id):
    logger.debug("Connecting to {} ID {}".format(beacon_hp, beacon_id))
    host_addr, host_port = beacon_hp.split(":")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(s)
    conn.connect( (host_addr, int(host_port)) )
    avax_handle_protocol(conn)


# Run ------------------------------------------------------------------------

# Load config and logger

avax_config = AVAXConfig()
logger = avax_config.logger()

node = Node()
node.Net = Network()

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.load_cert_chain(certfile=avax_config.get("staker_crt"), keyfile=avax_config.get("staker_key"))

p = avaxpython.parallel()

for i in range(len(beacons.beacon_ips[constants.MainnetID])):

    beacon_hp = beacons.beacon_ips[constants.MainnetID][i]
    beacon_id = beacons.beacon_ids[constants.MainnetID][i]

    avax_dispatch_host(beacon_hp, beacon_id)
    #f = p.go(avax_dispatch_host, beacon_hp, beacon_id)

    #print(f.result())

