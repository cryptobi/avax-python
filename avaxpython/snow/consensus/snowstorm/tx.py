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

from avaxpython.snow.choices.decidable import Decidable

class Tx(Decidable):

    # Dependencies is a list of transactions upon which this transaction
    # depends. Each element of Dependencies must be verified before Verify is
    # called on this transaction.

    # Similarly, each element of Dependencies must be accepted before this
    # transaction is accepted.
    def Dependencies(self):
        pass

    # InputIDs is a set where each element is the ID of a piece of state that
    # will be consumed if this transaction is accepted.

    # In the context of a UTXO-based payments system, for example, this would
    # be the IDs of the UTXOs consumed by this transaction
    def InputIDs(self):
        pass

    # Verify that the state transition this transaction would make if it were
    # accepted is valid. If the state transition is invalid, a non-nil error
    # should be returned.

    # It is guaranteed that when Verify is called, all the dependencies of
    # this transaction have already been successfully verified.
    def Verify(self):
        pass

    # Bytes returns the binary representation of this transaction.

    # This is used for sending transactions to peers. Another node should be
    # able to parse these bytes to the same transaction.
    def Bytes(self):
        pass

