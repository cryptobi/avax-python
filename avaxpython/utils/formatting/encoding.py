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

import cb58ref
from avaxpython.utils.hashing import hashing


class Encoding:

    # maximum length byte slice can be encoded as a string
    # using the CB58 encoding. Must be longer than the length
    # of an ID and longer than the length of a SECP256k1 private key
    # TODO: Reduce to a reasonable amount (e.g. 16 * 1024) after we
    # give users a chance to export very large keystore users to hex
    maxCB58EncodeSize = 2147483647
    hexPrefix         = "0x"
    checksumLen       = 4

    # Maximum length CB58 encoded string that can be decoded to bytes
    # This is different than [maxCB58EncodeSize] because each byte can express up
    # to 256 but each base 58 digit can express up to 58
    # The 10 is because there seems to be a floating point issue where the calculated
    # max decode size (using this formula) is slightly smaller than the actual
    maxCB58DecodeSize   = int(maxCB58EncodeSize * 4/3) + 10 # this is approximate
    errInvalidEncoding  = Exception("invalid encoding")
    errMissingChecksum  = Exception("input string is smaller than the checksum size")
    errBadChecksum      = Exception("invalid input checksum")
    errMissingHexPrefix = Exception("missing 0x prefix to hex encoding")

    # CB58 specifies the CB58 encoding format
    CB58 = 0
    # Hex specifies a hex plus 4 byte checksum encoding format
    Hex = 1

    # Default encoding when not specified
    defaultEncoding = CB58

    def __init__(self, e = defaultEncoding):
        self.enc = e

    def String(self):
        if self.enc == Encoding.Hex:
            return "hex"
        if self.enc == Encoding.CB58:
            return "cb58"
        
        raise Exception(f"Invalid encoding: {self.enc}")

    def __str__(self):
        return self.String()

    def valid(self):
        return self.enc in [Encoding.Hex, Encoding.CB58]

    def MarshalJSON(self):
        if not self.valid():
            return Encoding.errInvalidEncoding
        
        return bytes("\"" + self.String() + "\"", "utf-8")
    
    def UnmarshalJSON(self, b: bytes):
        strx = b.decode("utf-8")
        if strx == "null":
            return None
        
        lstr = strx.lower()

        if lstr == "\"hex\"":
            self.enc = Encoding.Hex
            return self.enc
        elif lstr == "\"cb58\"":
            self.enc = Encoding.CB58
            return self.enc
        
        return Encoding.errInvalidEncoding
        

    def Encode(self, bbytes: bytes) -> str:
        """Encode [bytes] to a string using the given encoding format
            [bytes] may be nil, in which case it will be treated the same
            as an empty slice"""
        
        if not self.valid():
            raise Encoding.errInvalidEncoding

        if self.enc == Encoding.CB58 and len(bbytes) > Encoding.maxCB58EncodeSize:
            raise Exception(f"byte slice length ({len(bbytes)}) > maximum for cb58 ({Encoding.maxCB58EncodeSize})")
        
        if self.enc == Encoding.Hex:
            return f"0x{bbytes.hex()}"
        if self.enc == Encoding.CB58:
            return cb58ref.cb58encode(bbytes)
        
        raise Exception(f"Invalid encoding {self.enc}")


    def Decode(encoding, sstr: str) -> bytes:
        """Decode [str] to bytes using the given encoding
            If [str] is the empty string, returns None"""
        
        if not encoding.valid():
            raise Encoding.errInvalidEncoding
        elif len(str) == 0:
            return None
        elif encoding.enc == CB58 and len(sstr) > Encoding.maxCB58DecodeSize:
            raise Exception(f"string length ({len(sstr)}) > maximum for cb58 ({Encoding.maxCB58DecodeSize})")
        
        
        decodedBytes = bytearray()

        if encoding.enc == Encoding.Hex:
            if not sstr.startswith(Encoding.hexPrefix):
                return Encoding.errMissingHexPrefix
            
            decodedBytes = hex.DecodeString(str[2:])
        if encoding.enc == Encoding.CB58:
            decodedBytes = base58.Decode(str)
        
        if len(decodedBytes) < Encoding.checksumLen:
            raise Encoding.errMissingChecksum
        
        rawBytes = decodedBytes[:len(decodedBytes)-Encoding.checksumLen]
        if len(rawBytes) > Encoding.maxCB58EncodeSize:
            raise Exception(f"byte slice length ({len(decodedBytes)}) > maximum for cb58 ({Encoding.maxCB58EncodeSize})")
    

        checksum = decodedBytes[len(decodedBytes)-Encoding.checksumLen:]
        if not checksum == hashing.Checksum(rawBytes, checksumLen):
            raise Encoding.errBadChecksum
        
        return rawBytes


    def HashEncode(self, bbytes: bytes) -> str:
        """Hash a bytes value using SHA256 and return the CB58 encoded digest."""
        digest_bytes = hashing.ComputeHash256(bbytes)
        return self.Encode(digest_bytes)

