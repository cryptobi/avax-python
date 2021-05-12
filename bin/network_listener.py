#!/usr/bin/python3
# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Find tutorials and use cases at https://crypto.bi

"""

Copyright (C) 2021 - crypto.bi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

Help support this Open Source project!
Donations address: X-avax1qr6yzjykcjmeflztsgv6y88dl0xnlel3chs3r4
Thank you!

"""

# --#--#--

from avaxpython.handlers.DEFAULT import DefaultHandler
import signal
import sys
import avaxpython
from avaxpython.main import params
from avaxpython.Config import Config as AVAXConfig
from avaxpython.network import ip
from avaxpython.utils.ip import IPDesc
from avaxpython.node.node import Node
from avaxpython.node.Config import Config as NodeConfig
from avaxpython.snow.handlers.json_printer import JSONPrinter

#
# Instructions
# ------------
#
# Before running network_listener.py for the first time:
#
# Download and build the official AVAX implementation in Go
# cd ~/go/src/github.com/ava-labs/
# git clone https://github.com/ava-labs/avalanchego.git
# cd avalanchego
#
# Run the Go client once to generate the needed certs and data directory.
#

# --------------------------------------------------------------------------------

# Good fortune ASCII-art header from avalanchego/main/main.go  
header = """
         _____               .__                       .__
        /  _  \___  _______  |  | _____    ____   ____ |  |__   ____    ,_ o
       /  /_\  \  \/ /\__  \ |  | \__  \  /    \_/ ___\|  |  \_/ __ \   / //\,
      /    |    \   /  / __ \|  |__/ __ \|   |  \  \___|   Y  \  ___/    \>> |
      \____|__  /\_/  (____  /____(____  /___|  /\___  >___|  /\___  >    \\
              \/           \/          \/     \/     \/     \/     \/
"""

print(header)

# --------------------------------------------------------------------------------

params.parseCmdLine()
node_config = params.Config

logger = avaxpython.config().logger()

avaxpython.config().set("handler", DefaultHandler())

stk_ip = ip.get_internal_ip()

node_config.StakingIP = IPDesc(stk_ip.ip, NodeConfig.STAKING_PORT)
node = Node(config=node_config)

def signal_handler(sig, frame):
    logger.info("Stopping the AVAX node.")
    node.Shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

node.Initialize(node_config)
node.Dispatch()
