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


from avaxpython.utils.ip import IPDesc
from avaxpython.utils import nlimits
from avaxpython.utils.hashing import hashing


class Packer:
    MaxStringLen = 65535
    ByteLen = 1
    ShortLen = 2
    IntLen = 4
    LongLen = 8
    BoolLen = 1

    errBadLength = Exception("packer has insufficient length for input")
    errNegativeOffset = Exception("negative offset")
    errInvalidInput = Exception("input does not match expected format")
    errBadType = Exception("wrong type passed")
    errBadBool = Exception("unexpected value when unpacking bool")

    def __init__(self, b):
        self.Bytes = b
        self.Offset = 0
        self.Errs = []

    def PackByte(p, val):

        if p.Errored():
            return

        barr = bytearray(p.Bytes)
        barr.extend(val.to_bytes(1, "big"))
        p.Bytes = bytes(barr)
        p.Offset += 1

    def UnpackByte(p):

        if p.Errored():
            return 0

        endoff = p.Offset + 1
        val = p.Bytes[p.Offset:endoff]
        p.Offset += 1
        return val

    def PackShort(p, val):
        if p.Errored():
            return

        barr = bytearray(p.Bytes)
        barr.extend(val.to_bytes(Packer.ShortLen, "big"))
        p.Bytes = bytes(barr)
        p.Offset += Packer.ShortLen

    def UnpackShort(p):
        if p.Errored():
            return 0

        endoff = p.Offset + Packer.ShortLen
        val = int.from_bytes(p.Bytes[p.Offset:endoff], "big")
        p.Offset += Packer.ShortLen
        return val

    def PackInt(p, val):
        if p.Errored():
            return

        barr = bytearray(p.Bytes)
        barr.extend(val.to_bytes(Packer.IntLen, "big"))
        p.Bytes = bytes(barr)

        p.Offset += Packer.IntLen

        return val

    def UnpackInt(p):
        if p.Errored():
            return 0

        endoff = p.Offset + Packer.IntLen
        val = int.from_bytes(p.Bytes[p.Offset:endoff], "big")
        p.Offset += Packer.IntLen
        return val

    def PackLong(p, val):
        if p.Errored():
            return

        barr = bytearray(p.Bytes)
        barr.extend(val.to_bytes(Packer.LongLen, "big"))
        p.Bytes = bytes(barr)
        p.Offset += Packer.LongLen

        return val

    def UnpackLong(p):
        if p.Errored():
            return 0

        endoff = p.Offset + Packer.LongLen
        val = int.from_bytes(p.Bytes[p.Offset:endoff], "big")
        p.Offset += Packer.LongLen
        return val

    def PackBool(p, b):
        if b:
            p.PackByte(1)
        else:
            p.PackByte(0)

    def UnpackBool(p):
        b = p.UnpackByte()

        if b == 0:
            return False
        elif b == 1:
            return True
        else:
            p.Add(f"Invalid bool {b}")
            return False

    def PackFixedBytes(p, bbytes):
        if p.Errored():
            return

        barr = bytearray(p.Bytes)
        barr.extend(bbytes)
        p.Bytes = bytes(barr)
        p.Offset += len(bbytes)

    def UnpackFixedBytes(p, size: int):
        if p.Errored():
            return None

        bbytes = p.Bytes[p.Offset: p.Offset + size]
        p.Offset += size
        return bbytes

    def PackBytes(p, dbytes):
        p.PackInt(int(len(dbytes)))
        p.PackFixedBytes(dbytes)

    def UnpackBytes(p):
        size = p.UnpackInt()
        return p.UnpackFixedBytes(int(size))

    def PackFixedByteSlices(p, byteSlices):
        p.PackInt(len(byteSlices))
        for bbytes in byteSlices:
            p.PackFixedBytes(bbytes)

    def UnpackFixedByteSlices(p, size: int):
        sliceSize = p.UnpackInt()
        bbytes = []
        i = int(0)
        while i < sliceSize and not p.Errored():
            bts = p.UnpackFixedBytes(size)
            bbytes.append(bts)
            i += 1

        return bbytes

    def Pack2DByteSlice(p, byteSlices):
        p.PackInt(len(byteSlices))
        for bbytes in byteSlices:
            p.PackBytes(bbytes)

    def Unpack2DByteSlice(p):
        sliceSize = p.UnpackInt()
        bbytes = []
        i = 0
        while i < sliceSize and not p.Errored():
            bts = p.UnpackBytes(sliceSize)
            bbytes.extend(bts)
            i += 1

        return bbytes

    def PackStr(p, dstr):
        strSize = len(dstr)
        if strSize > Packer.MaxStringLen:
            p.Add(Packer.errInvalidInput)

        p.PackShort(strSize)
        p.PackFixedBytes(bytes(dstr, "utf-8"))

    def UnpackStr(p):
        strSize = p.UnpackShort()
        bts = p.UnpackFixedBytes(int(strSize))

        return bts.decode("utf-8")

    def PackIP(p, ip: IPDesc):
        ipto16_a = ip.To16()

        barr = bytearray(ipto16_a)
        if ip.version == IPDesc.V4:
            barr[-6] = 0xff
            barr[-5] = 0xff

        ipto16 = bytes(barr)

        p.PackFixedBytes(ipto16)
        p.PackShort(ip.Port)

    def UnpackIP(p):
        ip = p.UnpackFixedBytes(16)
        port = p.UnpackShort()
        return IPDesc(IP=ip, Port=port)

    def PackIPs(p, ips):
        p.PackInt(len(ips))
        i = 0
        while i < len(ips) and not p.Errored():
            p.PackIP(ips[i])
            i += 1

    def UnpackIPs(p):
        sliceSize = p.UnpackInt()
        ips = []
        i = int(0)
        if i < sliceSize and not p.Errored():
            ips.append(p.UnpackIP())
            i += 1
        return ips

    def TryPackByte(packer, valIntf):
        packer.PackByte(val)

    def TryUnpackByte(packer):
        return packer.UnpackByte()

    def TryPackShort(packer, valIntf):
        packer.PackShort(valIntf)

    def TryUnpackShort(packer):
        return packer.UnpackShort()

    def TryPackInt(packer, valIntf):
        packer.PackInt(valIntf)

    def TryUnpackInt(packer):
        return packer.UnpackInt()

    def TryPackLong(packer, valIntf):
        packer.PackLong(valIntf)

    def TryUnpackLong(packer):
        return packer.UnpackLong()

    def TryPackHash(packer, valIntf):
        packer.PackFixedBytes(valIntf)

    def TryUnpackHash(packer):
        return packer.UnpackFixedBytes(hashing.HashLen)

    def TryPackHashes(packer, valIntf):
        packer.PackFixedByteSlices(valIntf)

    def TryUnpackHashes(packer):
        return packer.UnpackFixedByteSlices(hashing.HashLen)

    def TryPackAddr(packer, valIntf):
        packer.PackFixedBytes(valIntf)

    def TryUnpackAddr(packer):
        return packer.UnpackFixedBytes(hashing.AddrLen)

    def TryPackAddrList(packer, valIntf):
        packer.PackFixedByteSlices(valIntf)

    def TryUnpackAddrList(packer):
        return packer.UnpackFixedByteSlices(hashing.AddrLen)

    def TryPackBytes(packer, valIntf):
        packer.PackBytes(valIntf)

    def TryUnpackBytes(packer):
        return packer.UnpackBytes()

    def TryPack2DBytes(packer, valIntf):
        packer.Pack2DByteSlice(valIntf)

    def TryUnpack2DBytes(packer):
        return packer.Unpack2DByteSlice()

    def TryPackStr(packer, valIntf):
        packer.PackStr(valIntf)

    def TryUnpackStr(packer):
        return packer.UnpackStr()

    def TryPackIP(packer, valIntf):
        packer.PackIP(valIntf)

    def TryUnpackIP(packer):
        return packer.UnpackIP()

    def TryPackIPList(packer, valIntf):
        packer.PackIPs(valIntf)

    def TryUnpackIPList(packer):
        return packer.UnpackIPs()

    def Errored(packer):
        return len(packer.Errs) > 0

    def Add(packer, errors):
        for e in errors:
            packer.Errs.append(e)

    def Bytes(self):
        return self.Bytes
