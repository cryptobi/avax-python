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

from typing import List
from avaxpython.ids.ID import ID
from avaxpython import ids
from avaxpython.types import Uint32
from avaxpython.structured import AvaxStructured

errNilUTXOID = Exception("nil utxo ID is not valid")

class UTXOID(AvaxStructured):

    _avax_tags = [
        ("TxID", {"serialize": True, "json": "txID" }), 
        ("OutputIndex", {"serialize": True, "json": "outputIndex" }), 
    ]

    def __init__(self, txid: ID = ID(), output_index: Uint32 = 0, symbol: bool = False, idx: ID = ID()): 
	    self.TxID: ID = txid
	    self.OutputIndex = Uint32(output_index)
	    # Symbol is false if the UTXO should be part of the DB
	    self.Symbol: bool = symbol
	    # id is the unique ID of a UTXO, it is calculated from TxID and OutputIndex
	    self.id : ID = idx
    
    def InputSource(utxo):
        """InputSource returns the source of the UTXO that this input is spending"""
        return utxo.TxID, utxo.OutputIndex
    
    def InputID(utxo):
        """InputID returns a unique ID of the UTXO that this input is spending"""
        if utxo.id == ids.Empty():
            utxo.id = utxo.TxID.Prefix(int(utxo.OutputIndex))
        
        return utxo.id
        
    def Symbolic(utxo):
        """Symbolic returns if this is the ID of a UTXO in the DB, or if it is a symbolic input"""
        return utxo.Symbol
    
    def Verify(utxo):
        """Verify implements the verify.Verifiable interface"""
        return None
        
    def __str__(self):
        _d = {}
        for k, v in self._avax_tags:
            _d[k] = str(getattr(self, k))
        return str(_d)
    

class innerSortUTXOIDs:
    def __init__(self) -> None:
        self._arr : List[UTXOID] = []

    def Less(utxos, i : int, j: int) -> bool:
                
        if utxos._arr[i] > utxos._arr[i]:
            return False

        return True        
    

    def Len(utxos) -> int:
        return len(utxos._arr)

    def Swap(utxos, i: int, j: int):
        utxos[j], utxos[i] = utxos[i], utxos[j]


def SortUTXOIDs(utxos: List[UTXOID]):
    # TODO sort.Sort(innerSortUTXOIDs(utxos))
    pass

def IsSortedAndUniqueUTXOIDs(utxos: List[UTXOID]) -> bool:
    # TODO	
    return False

