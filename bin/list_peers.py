#!/usr/bin/python3

# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

# list_peers.py - List peers found on the AVAX network

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


import signal
import sys
import logging
from avaxpython.Config import Config as AVAXConfig
from avaxpython.network import ip
from avaxpython.utils.ip import IPDesc
from avaxpython.node.node import Node
from avaxpython.node.Config import Config as NodeConfig
from avaxpython.network.handlers.HostLister import HostLister


node_config = NodeConfig()
avax_config = AVAXConfig(log_level=logging.ERROR)
logger = avax_config.logger()

hl = HostLister(avax_config)
avax_config.set("network_handler", hl)

stk_ip = ip.get_internal_ip()
node_config.StakingIP = IPDesc(stk_ip.ip, NodeConfig.STAKING_PORT)

node = Node(avax_config=avax_config)

def signal_handler(sig, frame):
    logger.info("Stopping the AVAX node.")
    node.Shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

node.Initialize(node_config, avax_config)
node.Dispatch()
