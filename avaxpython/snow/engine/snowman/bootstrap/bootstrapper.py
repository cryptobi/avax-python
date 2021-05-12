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


from avaxpython.snow.engine.common.config import Config as CommonConfig
from avaxpython.snow.engine.common.boostrapper import Bootstrapper as CommonBootstrapper
from avaxpython.snow.engine.common.fetcher import Fetcher
from avaxpython.snow.engine.snowman.block.vm import ChainVM


# Parameters for delaying bootstrapping to avoid potential CPU burns
initialBootstrappingDelay = 500 * 0.001 # seconds
maxBootstrappingDelay     = 60


class Config(CommonConfig):
    """Bootstrapper-specific config"""
    def __init__(self, ctx, validators, beacons, samplek, startupalpha, alpha, sender, bootstrapable, subnet, delay, retrybootstrap, rbmaxattempts):
        super().__init__(ctx, validators, beacons, samplek, startupalpha, alpha, sender, bootstrapable, subnet, delay, retrybootstrap, rbmaxattempts)
        # Blocked tracks operations that are blocked on blocks
        self.Blocked  = []
        self.VM = None
        self.Bootstrapped = super().IsBootstrapped


class Bootstrapper(Config, CommonBootstrapper, Fetcher):

    def __init__(self, vm, ctx):

        Config.__init__(self, ctx, [], 0, 0, 0, None, False, None, 0, 0, 0, 0)
        CommonBootstrapper.__init__(self, None, None, None, None, None, None, None, None, None, None, None)
        Fetcher.__init__(self, 0, 0, None)
        # Blocked tracks operations that are blocked on blocks
        self.Blocked = []
        self.VM: ChainVM = vm
        self.Ctx = ctx
        self.Bootstrapped = None

        # true if all of the vertices in the original accepted frontier have been processed
        self.processedStartingAcceptedFrontier = False

        # number of state transitions executed
        self.executedStateTransitions = 0 
        self.delayAmount = 0