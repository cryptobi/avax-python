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


class GenesisAsset:
    _avax_tags = [
        ("Alias", { "serialize": True}),
        ("CreateAssetTx", { "serialize": True}),
    ]

    def __init__(self) -> None:        
        self.Alias = str()
        self.CreateAssetTx = CreateAssetTx()


class Genesis:
    _avax_tags = [
        ("Txs", { "element_type": GenesisAsset, "serialize": True}),
    ]

    def __init__(self) -> None:        
        self.Txs = Slice()

    def Less(self, i: int, j: int) -> bool:
        return strings.Compare(g.Txs[i].Alias, g.Txs[j].Alias) == -1

    def Len(self) -> int:
        return len(g.Txs)

    def Swap(self, i: int, j: int):
        g.Txs[j], g.Txs[i] = g.Txs[i], g.Txs[j]

    def Sort(self):
        sort.Sort(g)

    def IsSortedAndUnique(self) -> bool:
        return utils.IsSortedAndUnique(g)

