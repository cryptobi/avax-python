#!/bin/sh

# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

#

# Copyright © 2021 ojrdev

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# --#--#--


ppath=`pwd`

PYTHONPATH=$ppath
PYTHONPATH=$PYTHONPATH:$ppath/3rdparty/pysha3/
PYTHONPATH=$PYTHONPATH:$ppath/3rdparty/pysha3/build/lib.linux-x86_64-3.8/_pysha3.cpython-38-x86_64-linux-gnu.so
PYTHONPATH=$PYTHONPATH:$ppath/3rdparty/bip_utils/
PYTHONPATH=$PYTHONPATH:$ppath/3rdparty/py_crypto_hd_wallet/py_crypto_hd_wallet/
PYTHONPATH=$PYTHONPATH:$ppath/3rdparty/python-mnemonic/mnemonic/
PYTHONPATH=$PYTHONPATH:$ppath/3rdparty/cb58ref/
PYTHONPATH=$PYTHONPATH:$ppath/3rdparty/x509-parser/

export PYTHONPATH
