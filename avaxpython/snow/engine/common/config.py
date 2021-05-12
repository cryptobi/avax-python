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

from avaxpython.snow.context import Context

class Config:
    """Common configuration base class. Used by consensus engines."""
    def __init__(self, ctx, validators, beacons, samplek, startupalpha, alpha,
    sender, bootstrapable, subnet, delay, retrybootstrap, rbmaxattempts):
        self.Ctx : Context = ctx
        self.Validators= validators
        self.Beacons = beacons
        self.SampleK = samplek
        self.StartupAlpha = startupalpha
        self.Alpha = alpha
        self.Sender = sender
        self.Bootstrapable = bootstrapable
        self.Subnet = subnet
        self.Delay = delay

        # Should Bootstrap be retried
        self.RetryBootstrap = retrybootstrap
        # Max number of times to retry bootstrap
        self.RetryBootstrapMaxAttempts = rbmaxattempts

    # Context implements the Engine interface
    def Context(self) -> Context:
        return self.Ctx

    # IsBootstrapped returns true iff this chain is done bootstrapping
    def IsBootstrapped(self) -> bool:
        return self.Ctx.IsBootstrapped()
