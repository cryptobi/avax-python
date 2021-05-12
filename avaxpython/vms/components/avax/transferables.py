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
from avaxpython.vms.components.avax.asset import Asset
from avaxpython.vms.components.verify.verification import Verifiable
from avaxpython.vms.components.avax.utxo import UTXO
from avaxpython.vms.components.avax.utxo_id import UTXOID
from avaxpython.structured import AvaxStructured

errNilTransferableOutput   = Exception("nil transferable output is not valid")
errNilTransferableFxOutput = Exception("nil transferable feature extension output is not valid")
errOutputsNotSorted        = Exception("outputs not sorted")

errNilTransferableInput   = Exception("nil transferable input is not valid")
errNilTransferableFxInput = Exception("nil transferable feature extension input is not valid")
errInputsNotSortedUnique  = Exception("inputs not sorted and unique")


class Amounter:
    """Amounter is a data structure that has an amount of something associated with it"""
    _avax_interface = True

    def __init__(self) -> None:
        self.amt = 0

    def Amount(self) -> Uint64:
        """Amount returns how much value this element represents of the asset in its transaction"""
        return self.amt


class TransferableIn(Verifiable, Amounter):
    _avax_interface = True
    """TransferableIn is the interface a feature extension must provide to transfer
    value between features extensions.
    """
    def __init__(self) -> None:
        Verifiable.__init__(self)
        Amounter.__init__(self)


class TransferableOut:
    _avax_interface = True
    """TransferableOut is the interface a feature extension must provide to transfer
    value between features extensions.
    """


class TransferableOutput(AvaxStructured):
    _avax_tags = [
        ("Asset", {"serialize": True, "json": "" }), 
        ("Out", {"serialize": True, "json": "output" }), 
    ]

    def __init__(self) -> None:            
        self.Asset = Asset()
        self.Out = TransferableOut()
    
    def Output(self):
        """Output returns the feature extension output that this Output is using."""
        return self.Out

    # Verify implements the verify.Verifiable interface
    def Verify(self):
    
        if self.Out == None:
            raise errNilTransferableFxOutput
        else:
            return None
    

class innerSortTransferableOutputs:

    def __init__(self) -> None:
        self.outs = Slice([TransferableOutput()])
        self.codec = None

    def Less(self, i: int, j: int) -> bool:
        iOut = self.outs.outs[i]
        jOut = self.outs.outs[j]

        iAssetID = iOut.AssetID()
        jAssetID = jOut.AssetID()

        a_diff = iAssetID[:] - jAssetID[:]
        if a_diff == -1:
            return True
        elif a_diff == 1:
            return False

        iBytes = outs.codec.Marshal(codecVersion, iself.Out)        
        jBytes = outs.codec.Marshal(codecVersion, jself.Out)
        
        jb_diff = iBytes - jBytes
        return jb_diff == -1
        
    def Len(self) -> int:
        return len(self.outs.outs)

    def Swap(self, i: int, j: int):
        o = self.outs.outs
        o[j], o[i] = o[i], o[j]


def SortTransferableOutputs(outs, codec_manager):
    """SortTransferableOutputs sorts output objects"""	
    

def IsSortedTransferableOutputs(outs, codec_manager):
    """IsSortedTransferableOutputs returns true if output objects are sorted"""	
    

class TransferableInput(AvaxStructured):
    _avax_tags = [
        ("UTXOID", {"serialize": True, "json": "" }), 
        ("Asset", {"serialize": True, "json": "" }), 
        ("In", {"serialize": True, "json": "input" }), 
    ]

    def __init__(self) -> None:
        
        self.UTXOID = UTXOID()
        self.Asset  = Asset()
        self.In = TransferableIn()
    
    def Input(self) -> TransferableIn:
        """Input returns the feature extension input that this Input is using."""
        return self.In
    
    def Verify(self):
        """Verify implements the verify.Verifiable interface"""
    
        if self.In == None:
            raise errNilTransferableFxInput




class innerSortTransferableInputs:

    def Less(self, i: int, j: int) -> bool:
        iID, iIndex = ins[i].InputSource()
        jID, jIndex = ins[j].InputSource()

        ij_d = iID[:] - jID[:]
        
        if ij_d == -1:
            return True
        elif ij_d == 0:
            return iIndex < jIndex
        else:
            return False

    def Len() -> int:
        return len(ins)

    def Swap(i: int, j: int):
        ins[j], ins[i] = ins[i], ins[j]


def SortTransferableInputs(ins):
    pass

def IsSortedAndUniqueTransferableInputs(ins):
    pass


class innerSortTransferableInputsWithSigners:
    
    def __init__(self):	
        self.ins = None
        self.signers = None

    def Less(self, i: int, j: int) -> bool:
        iID, iIndex = ins.ins[i].InputSource()
        jID, jIndex = ins.ins[j].InputSource()

        ij_d = iID[:] - jID[:]
        if ij_d == -1:
            return True
        if ij_d == 0:
            return iIndex < jIndex
        else:
            return False
    
    def Len(self) -> int:
        return len(ins.ins)

    def Swap(self, i: int, j: int):
        ins.ins[j], ins.ins[i] = ins.ins[i], ins.ins[j]
        ins.signers[j], ins.signers[i] = ins.signers[i], ins.signers[j]
    

def SortTransferableInputsWithSigners(ins, signers):
    """SortTransferableInputsWithSigners sorts the inputs and signers based on the input's utxo ID"""
    pass


def IsSortedAndUniqueTransferableInputsWithSigners(ins, signers) -> bool:
    """IsSortedAndUniqueTransferableInputsWithSigners returns true if the inputs are sorted and unique"""
    pass

def VerifyTx(feeAmount, feeAssetID, allIns, codec_manager):
    """VerifyTx verifies that the inputs and outputs flowcheck, including a fee. 
    Additionally, this verifies that the inputs and outputs are sorted."""
    pass
