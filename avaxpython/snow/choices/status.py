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

from avaxpython.utils.wrappers.Packer import Packer

errUnknownStatus = Exception("unknown status")


class Status:

# List of possible status values
# [Unknown] Zero value, means the status is not known
# [Processing] means the operation is known, but hasn't been decided yet
# [Rejected] means the operation will never be accepted
# [Accepted] means the operation was accepted

    Unknown = 0
    Processing = 1
    Rejected = 2
    Accepted = 3

    def __init__(self, status=0):
        self.status = status

    def MarshalJSON(self) -> bytes:
        if not self.Valid():
            return None
        
        return ("\"" + self.String() + "\"").encode("utf-8")


    def UnmarshalJSON(self, b: bytes):
        b_str = b.decode("utf-8")

        if b_str == "null":
            return None
        
        if b_str == "\"Unknown\"":
            self.status = Status.Unknown
        elif b_str == "\"Processing\"":
            self.status = Processing
        elif b_str == "\"Rejected\"":
            self.status = Rejected
        elif b_str == "\"Accepted\"":
            self.status = Accepted
        else:
            raise errUnknownStatus
        
        return None


    def Fetched(self):
        """Fetched returns true if the status has been set."""
        if self.status == Status.Processing:
            return True
        else:
            return self.Decided()
        

    def Decided(self):
        """Decided returns true if the status is Rejected or Executed."""
        return self.status in [Status. Rejected, Status.Accepted]
            

    def Valid(self):
        """Valid returns None if the status is a valid status."""
        return self.status in [Status.Unknown, Status.Processing, Status.Rejected, Status.Accepted]
            

    def String(self):
        if self.status == Status.Unknown:
            return "Unknown"
        elif self.status == Status.Processing:
            return "Processing"
        elif self.status == Status.Rejected:
            return "Rejected"
        elif self.status == Status.Accepted:
            return "Accepted"
        else:
            return "Invalid status"



    def Bytes(self):
        """Bytes returns the byte repr. of this status"""
        p = Packer()
        p.PackInt(int(self.status))
        return p.Bytes

