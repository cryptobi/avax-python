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

from avaxpython.types import *
from avaxpython.ids.ID import ID
from avaxpython.ids.ShortID import ShortID
from avaxpython.structured import AvaxStructured

errBadSubnetID = ValueError("subnet ID can't be primary network ID")

class Validator(AvaxStructured):
    """Validator is a validator."""
    _avax_tags = [
		("NodeID", { "json": "version", "json" : "nodeID" }),
		("Start", { "serialize": True, "json" : "start" }),
		("End", { "serialize": True, "json":"end"}),
		("Wght", { "serialize": True, "json":"weight"}),
	]

    def __init__(self) -> None:        
        # Node ID of the validator
        self.NodeID = ShortID()

        # Unix time this validator starts validating
        self.Start = Uint64()

        # Unix time this validator stops validating
        self.End = Uint64()

        # Weight of this validator used when sampling
        self.Wght = Uint64()



class SubnetValidator:
    """Validator is a validator."""
    _avax_tags = [
		("Validator", { "json": "version" }),
		("Subnet", { "serialize": True, "json" : "subnet" }),
	]

    def __init__(self) -> None:
        self.Validator = Validator()        
        self.Subnet = ID()

