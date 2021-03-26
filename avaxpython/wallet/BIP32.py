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


# BIP32 related functions

from bip_utils import Bip32
from bip_utils.bip.bip_keys import BipPublicKey
from avaxpython.wallet.BIP44 import Bip44AVAXMainNet
import hashlib
import cb58ref
from avaxpython.wallet import bech32
import binascii

def key_from_seed(seed):
    """Return master private key from this seed"""
    bip32_ctx = Bip32.FromSeed(seed)

    return bip32_ctx


def get_preferred_HRP(networkID):
    return "avax"


def address_from_publickey_bytes(bts):
    m = hashlib.sha256()
    m.update(bts)
    sh256 = m.digest()
    n = hashlib.new('ripemd160')
    n.update(sh256)    
    return n.digest()


def address_from_publickey(pk):
    m = hashlib.sha256()
    return address_from_publickey_bytes(pk.ToBytes())
    

def address_to_string(hrp, chainId, addr):
    dta = bech32.convertbits(addr, 8, 5, True)
    ret = bech32.bech32_encode(hrp, dta, bech32.Encoding.BECH32)
    return "{}-{}".format(chainId, ret)


def derive_master_key(masterKey, derivationPath):
    return masterKey.DerivePath(derivationPath)


def get_address_for_index(masterKey: Bip32, changePath: str, index: int, chainId, networkID) -> str:

    derivationPath = f"{changePath}/{index}"    
    key = derive_master_key(masterKey, derivationPath) # as HDKey
    public_key = BipPublicKey(key, Bip44AVAXMainNet)
    pk = public_key.RawCompressed()
    addr = address_from_publickey(pk)
    return address_to_string(networkID, chainId, addr)

        

