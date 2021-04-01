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

import sys
import logging
from os import path
from pathlib import Path

# General avaxpython configuration.
# Specific to avax-python, not part of the AVAX implementation.

# Default AVAX key size
KEY_SIZE = 256
MAX_WORKERS = 1
NETWORK_WORKERS=8
DEFAULT_WORKER_MODE = "process" # process or thread
key_filename = "staker.key"
crt_filename = "staker.crt"
DEFAULT_BUFFIZ = 8192
GO_SRC_PATH = "go/src/github.com/ava-labs/avalanchego"
GO_BEACONS_PATH = "genesis/beacons.go"
AVAX_DOTDIR = ".avalanchego"
AVAX_PYTHON_VERSION = "avax-python/0.0.1"
AVAX_NETWORK_VERSION = "avalanche/1.3.1"

class Config:

    def __init__(self, log_level=None):
        # ParallelDriver to use when not specified
        self.default_parallel_module = 'thread'
        self.default_config()
        self.default_logger(log_level)


    def default_config(self):

        self.conf = {}
        self.set("home_dir", str(Path.home()))
        self.set("version", AVAX_PYTHON_VERSION)
        self.set("avax_sources", path.join(self.get("home_dir"), GO_SRC_PATH))
        self.set("avax_home", path.join(self.get("home_dir"), AVAX_DOTDIR))
        self.set("certs_dir", path.join(self.get("avax_home"), "staking"))
        self.set("staker_key", path.join(self.get("certs_dir"), key_filename))
        self.set("staker_crt", path.join(self.get("certs_dir"), crt_filename))
        self.set("beacons_source", path.join(self.get("avax_sources"), GO_BEACONS_PATH))
        self.set("logging_level", logging.DEBUG)
        self.set("logging_format", '%(asctime)s %(levelname)s : %(message)s')


    def set(self, k, v):
        self.conf[k] = v

        return self.conf


    def get(self, k):
        if k in self.conf:
            return self.conf[k]

        return None


    def logger(self):
        if self._logger == None:
            self.default_logger()
        
        return self._logger


    def default_logger(self, level=None):

        if level is None:
            level = self.get("logging_level")
                        
        self._logger = logging.getLogger()
        self._logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(self.get("logging_format"))
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        return self._logger