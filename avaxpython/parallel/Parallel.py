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

import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import inspect
from avaxpython import Config


class Parallel:

    _tp_map = {
        'thread': ThreadPoolExecutor,
        'process': ProcessPoolExecutor
    }    


    def __init__(self, tp = Config.DEFAULT_WORKER_MODE):

        if not tp in Parallel._tp_map:
           raise Exception("Unknown parallelization type.")

        self.mode = tp
        
        cls = Parallel._tp_map[tp]
        self.cls = cls

        # general worker
        self.tp = cls(max_workers = Config.MAX_WORKERS)

        # network worker
        self.netp = cls(max_workers = Config.NETWORK_WORKERS)


    def executor(self):
        """Returns the globally configured Executor class."""
        return self.cls


    def worker(self):
        """Returns the general worker Executor instance."""
        return self.tp


    def net_worker(self):
        """Returns the network-specific Executor instance."""
        return self.netp


    def go(self, fn, *args, **kwargs):
        """Launches a new thread outside of the general and network Executor workers' control."""

        def _f1():
            fn(*args, **kwargs)

        if self.mode == "thread":
            t1 = threading.Thread(target = _f1)
            t1.start()
        elif self.mode == "process":
            p1 = multiprocessing.Process(target=_f1)
            p1.start()
        else:
            raise Exception(f"Unknown parallelization mode : {self.mode}")

