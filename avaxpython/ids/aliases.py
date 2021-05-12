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

from typing import Dict, List
from avaxpython.ids.ID import ID

class Aliaser:
    """Aliaser allows one to give an ID aliases and lookup the aliases given to an
    ID. An ID can have arbitrarily many aliases; two IDs may not have the same
    alias."""
    def __init__(self):        
        self.dealias: Dict[str, ID] = {}
        self.aliases: Dict(ID, List[str]) = {}

    def Initialize(self):
        """Initialize the aliaser to have no aliases"""
        self.dealias = {}
        self.aliases = {}
        
    def Lookup(self, alias: str) -> ID:
        """Lookup returns the ID associated with alias"""
        self.lock.RLock()
        if alias in self.dealias:
            return self.dealias[alias]

        return None
        
    def Aliases(self, id: ID):
        if id in self.aliases:
            return self.aliases[id]

        return []
        
    def PrimaryAlias(self, id: ID) -> str:
        """PrimaryAlias returns the first alias of [id]"""    

        if id in self.aliases:
            aliases = self.aliases[id]
            return aliases[0]
    
        return None
    
    def Alias(self, id: ID, alias: str):
        """Alias gives [id] the alias [alias]"""
        
        if alias in self.dealias:    
            self.dealias[alias] = id
            if id not in self.aliases:
                self.aliases[id] = []

            self.aliases[id].append(alias)
    
    def RemoveAliases(self, id: ID):
        """RemoveAliases of the provided ID"""    

        delete(self.aliases[id])

        for alias in self.aliases[id]:
            delete(self.dealias[alias])
