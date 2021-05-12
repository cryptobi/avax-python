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

import avaxpython
from avaxpython.ids.ID import ID

class Manager:
    """Manager is a factory class for VM's registered under certain ID's and aliases"""

    def __init__(self):
        self.vmFactories = {}
        self.aliases = {}
        self.dealias = {}

    def GetVMFactory(self, idx):
        s_idx = str(idx)
        if s_idx in self.vmFactories:
            return self.vmFactories[s_idx]
        raise Exception(f"No vm with ID '{s_idx}' has been registered")

    def RegisterVMFactory(self, idx: ID, vmf):
        self.vmFactories[str(idx)] = vmf        
        self.Alias(idx, str(idx))

    def Lookup(self, alias):
        
        if alias in self.dealias:
            return self.dealias[alias]

        return None

    def Aliases(self, idx):
        if idx in self.aliases:
            return self.aliases[idx]
        return set()

    def Alias(self, idx, alias):
        if idx not in self.aliases:
            self.aliases[idx] = set()
    
        if alias not in self.dealias:
            self.dealias[alias] = set()

        self.aliases[idx].add(alias)
        self.dealias[alias] = idx

    def __str__(self):
        d = {
            'aliases': self.aliases,
            'dealias': self.dealias,
            'vmFactories' : self.vmFactories
        }

        return str(d)