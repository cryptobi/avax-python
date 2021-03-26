#!/usr/bin/python3

# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

# avax.py - Standalone experimental AVAX client. Not a full node, just a passive network listener.

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


from avaxpython.Config import Config as AVAXConfig
from avaxpython.node.node import Node
from avaxpython.node.Config import Config as NodeConfig


#
# Getting ready to run avax.py :
#
# Download and build the official AVAX implementation in Go
# cd ~/go/src/github.com/ava-labs/
# git clone https://github.com/ava-labs/avalanchego.git
# cd avalanchego
#
# Run the Go client once to generate the needed certs and data directory.
#

node_config = NodeConfig()
avax_config = AVAXConfig()
logger = avax_config.logger()
node = Node(avax_config=avax_config)
node.Initialize(node_config, avax_config)
node.Dispatch()
