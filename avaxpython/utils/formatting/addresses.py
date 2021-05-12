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
# 

from typing import Tuple, List

addressSep = "-"


def FormatAddress(chainIDAlias: str, hrp: str, addr: bytes) -> str:
    """FormatAddress takes in a chain prefix, HRP, and byte slice to produce a string for an address."""
    addr_str = FormatBech32(hrp, addr)	
    return f"{chainIDAlias}{addressSep}{addr_str}"


# ParseBech32 takes a bech32 address as input and returns the HRP and data
# section of a bech32 address
def ParseBech32(addrStr: str) -> Tuple[str, bytes]:
	rawHRP, decoded = bech32.Decode(addrStr)	
	addrBytes = bech32.ConvertBits(decoded, 5, 8, True)	
	return rawHRP, addrBytes


# ParseAddress takes in an address string and splits returns the corresponding
# parts. This returns the chain ID alias, bech32 HRP, address bytes, and an
# error if it occurs.
def ParseAddress(addrStr: str) -> Tuple[str, str, bytes]:
	addressParts = addrStr.split(addressSep, 2)
	if len(addressParts) < 2:
		raise Exception(f"no separator found in address")
	
	chainID = addressParts[0]
	rawAddr = addressParts[1]

	hrp, addr = ParseBech32(rawAddr)
	return chainID, hrp, addr


# FormatBech32 takes an address's bytes as input and returns a bech32 address
def FormatBech32(hrp: str, payload: bytes) -> str:
	fiveBits = bech32.ConvertBits(payload, 8, 5, True)	
	addr = bech32.Encode(hrp, fiveBits)
	return addr

