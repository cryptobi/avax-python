#!/usr/bin/python3

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


# Print out AVAX addresses for a given mnemonic phrase
# Usage: addresses_from_mnemonic.py <phrase> 


import sys
from mnemonic import Mnemonic
from avaxpython.wallet import generator, BIP32
from avaxpython.wallet import Config as WalletConfig
from avaxpython import Config
from bip_utils import Bip32
import json

# Set how many addresses to generate starting from the HD key.
# The TypeScript wallet generates 512 initial addresses (I think)
# You may increase this to your liking.
ADDRESS_COUNT = 10

sample_wallet = next(generator.generate(1, Config.KEY_SIZE))
word_length = len(sample_wallet.split(" "))

if len(sys.argv) != word_length+1:
    print("Invalid phrase length provided. Got {} expected {}.".format(len(sys.argv)-1, word_length))
    exit(1)

seed = Mnemonic("english").to_seed(" ".join(sys.argv[1:]), passphrase="")

accountHdKey = Bip32.FromSeedAndPath(seed, WalletConfig.AVA_ACCOUNT_PATH)

output = []

for index in range(ADDRESS_COUNT):
    addr = BIP32.get_address_for_index(accountHdKey, '0', index, "X", "avax")
    output.append(addr)

print(json.dumps(output))
