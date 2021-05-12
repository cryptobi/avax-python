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

class Params:

    def __init__(self):
        # Transaction fee
        self.TxFee=0
        # Transaction fee for transactions that create new state
        self.CreationTxFee=0
        # Staking uptime requirements
        self.UptimeRequirement=0.0
        # Minimum stake, in nAVAX, required to validate the primary network
        self.MinValidatorStake=0
        # Maximum stake, in nAVAX, allowed to be placed on a single validator in
        # the primary network
        self.MaxValidatorStake=0
        # Minimum stake, in nAVAX, that can be delegated on the primary network
        self.MinDelegatorStake=0
        # Minimum delegation fee, in the range [0, 1000000], that can be charged
        # for delegation on the primary network.
        self.MinDelegationFee=0
        # MinStakeDuration is the minimum amount of time a validator can validate
        # for in a single period.
        self.MinStakeDuration=0 # TODO time.Duration
        # MaxStakeDuration is the maximum amount of time a validator can validate
        # for in a single period.
        self.MaxStakeDuration=0 # TODO time.Duration
        # StakeMintingPeriod is the amount of time for a consumption period.
        self.StakeMintingPeriod=0 # TODO time.Duration
        # EpochFirstTransition is the time that the transition from epoch 0 to 1
        # should occur.
        self.EpochFirstTransition=0 # TODO time.Time
        # EpochDuration is the amount of time that an epoch runs for.
        self.EpochDuration=0 # TODO time.Duration
        # Time that Apricot phase 0 rules go into effect
        self.ApricotPhase0Time=0 # TODO time.Time



