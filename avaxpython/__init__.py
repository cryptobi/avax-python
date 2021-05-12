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

from avaxpython.parallel import Parallel
from avaxpython.Config import Config
from avaxpython.types import *

__parallel = None
__config = None

def parallel(md = Config.DEFAULT_WORKER_MODE):

    """

    Parallelization singleton. 
    Loads an Executor the first time using the specified mode. 
    Then on future calls mode parameter is ignored.

    """

    global __parallel

    if __parallel == None:
        __parallel = Parallel.Parallel(md)

    return __parallel

def config():
    """Singleton access point for global config.
    Synchronize this in the future."""
    global __config

    if not __config:
         __config = Config()

    return __config 

def set_config(cnf):
    """Singleton access point for global config.
    Synchronize this in the future."""
    global __config

    __config = cnf

    return __config     