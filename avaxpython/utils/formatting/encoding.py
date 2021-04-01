# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--
# 


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

    @staticmethod
    def String(enc):
        if enc == Encoding.Hex:
            return "hex"
        if enc == Encoding.CB58:
            return "cb58"
        else:
            raise Exception(f"Invalid encoding: {enc}")

    @staticmethod
    def valid(enc):
        return enc == Encoding.Hex or enc == Encoding.CB58
