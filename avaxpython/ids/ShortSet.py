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


# # ShortSet is a set of ShortIDs

class ShortSet:

    minShortSetSize = 16
    _set = {}

    def __init__(self):
        pass

    # Add all the ids to this set, if the id is already in the set, nothing happens
    def Add(self, idList):
        self._set.update(idList)

    # Union adds all the ids from the provided sets to this set.
    def Union(self, idSet):
        self._set = self._set.union(idSet)

    # Contains returns true if the set contains this id, false otherwise
    def Contains(self, id):
        return id in self._set

    # Len returns the number of ids in this set
    def Len(self):
        return len(self._set)

    # Remove all the id from this set, if the id isn't in the set, nothing happens
    def Remove(self, idList):
        self._set.difference_update(idList)

    # Clear empties this set
    def Clear(self):
        self._set.clear()

    # CappedList returns a list of length at most [size].
    # Size should be >= 0. If size < 0, returns nil.
    def CappedList(self, size):
        return list(self._set[0 : size-1])

    # List converts this set into a list
    def List(self):
        return list(self._set)

    # Equals returns true if the sets contain the same elements
    def Equals(self, oIDs):
        return self._set == set(oIDs)

    # String returns the string representation of a set
    def String(self):
        return str(self._set)
