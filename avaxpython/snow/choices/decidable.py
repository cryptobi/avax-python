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

from avaxpython.ids.ID import ID as LongID


class Decidable:
    """Decidable represents element that can be decided.
    Decidable objects are typically thought of as either transactions, blocks, or vertices.
    """
    def __init__(self, idx: LongID = LongID()):
        self.id: LongID = idx

    def ID(self) -> LongID:
        """    ID returns a unique ID for this element.
        Typically, this is implemented by using a cryptographic hash of a
        binary representation of this element. An element should return the same
        IDs upon repeated calls.
        """
        return self.id

    def Accept(self):
        """    Accept this element.
        This element will be accepted by every correct node in the network.
        """
        
    def Reject(self):
        """    Reject this element.
        This element will not be accepted by any correct node in the network.
        """

    def Status(self) -> int:
        """    Status returns this element's current status.
        If Accept has been called on an element with this ID, Accepted should be
        returned. Similarly, if Reject has been called on an element with this
        ID, Rejected should be returned. If the contents of this element are
        unknown, then Unknown should be returned. Otherwise, Processing should be returned."""        
