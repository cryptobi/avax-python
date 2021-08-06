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


# AVAX BIP44 related functions

from bip_utils.conf.bip44_coins import Bip44Coin
from bip_utils.conf.bip_coin_conf import Bip32Conf
from bip_utils.conf.bip_coin_conf_helper import *
from bip_utils.addr import P2PKH


class AVAXConf:
    """ Class container for AVAX configuration. """

    # Names
    NAMES             = CoinNames("AVAX"        , "AVAX")

    # Test names
    TEST_NAMES        = CoinNames("AVAX TestNet", "tAVAX")

    # BIP44 net versions (same of BIP32)
    BIP44_KEY_NET_VER = Bip32Conf.KEY_NET_VER
    # BIP49 net versions (ypub / yprv) - (upub / uprv)
    BIP49_KEY_NET_VER = NetVersions(KeyNetVersions(b"049d7cb2", b"049d7878"),
                                    KeyNetVersions(b"044a5262", b"044a4e28"))
    # BIP84 net versions (zpub / zprv) -  (vpub / vprv)
    BIP84_KEY_NET_VER = NetVersions(KeyNetVersions(b"04b24746", b"04b2430c"),
                                    KeyNetVersions(b"045f1cf6", b"045f18bc"))

    # Versions for P2PKH address
    P2PKH_NET_VER     = NetVersions(b"\x00", b"\x6f")
    # Versions for P2SH address
    P2SH_NET_VER      = NetVersions(b"\x05", b"\xc4")
    # Versions for P2WPKH address
    P2WPKH_NET_VER    = NetVersions("bc", "tb")
    # WIF net version
    WIF_NET_VER       = NetVersions(b"\x80", b"\xef")



Bip44AVAXMainNet = Bip44Coin(coin_conf  = AVAXConf,
                                is_testnet = False,
                                addr_cls   = P2PKH)
