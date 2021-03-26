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

class Packer:

    MaxStringLen = nlimits.limits(nlimits.c_uint16)[1]
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

        p.Bytes[p.Offset] = val
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

        binary.BigEndian.PutUint16(p.Bytes[p.Offset:], val)
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

        binary.BigEndian.Putint(p.Bytes[p.Offset:], val)
        p.Offset += Packer.IntLen


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

        binary.BigEndian.PutUint64(p.Bytes[p.Offset:], val)
        p.Offset += Packer.LongLen


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
            return false
        elif b == 1:
            return true
        else:
            p.Add(errBadBool)
            return false
    

    def PackFixedBytes(p, bytes):
        if p.Errored():
            return
    
        copy(p.Bytes[p.Offset:], bytes)
        p.Offset += len(bytes)


    def UnpackFixedBytes(p, size):
        if p.Errored():
            return None

        bytes = p.Bytes[p.Offset : p.Offset+size]
        p.Offset += size
        return bytes


    def PackBytes(p, bytes):
        p.PackInt(int(len(bytes)))
        p.PackFixedBytes(bytes)


    def UnpackBytes(p):
        size = p.UnpackInt()
        return p.UnpackFixedBytes(int(size))


    def PackFixedByteSlices(p, byteSlices):
        p.PackInt(int(len(byteSlices)))
        for _, bytes in byteSlices:
            p.PackFixedBytes(bytes)


    def UnpackFixedByteSlices(p, size):
        sliceSize = p.UnpackInt()
        bytes = bytes([])
        i = int(0)
        while i < sliceSize and not p.Errored():
            bytes.append(p.UnpackFixedBytes(size))
            i += 1
        
        return bytes
    

    def Pack2DByteSlice(p, byteSlices):
        p.PackInt(int(len(byteSlices)))
        for _, bytes in byteSlices:
            p.PackBytes(bytes)


    def Unpack2DByteSlice(p):
        sliceSize = p.UnpackInt()
        bytes = bytes([])
        i = int(0)
        while i < sliceSize and not p.Errored():
            bytes = append(bytes, p.UnpackBytes())
            i += 1

        return bytes


    def PackStr(p, str):
        strSize = len(str)
        if strSize > MaxStringLen:
            p.Add(Packer.errInvalidInput)

        p.PackShort(uint16(strSize))
        p.PackFixedBytes([])


    def UnpackStr(p):
        strSize = p.UnpackShort()
        return str(p.UnpackFixedBytes(int(strSize)))

    
    def PackIP(p, ip):
        p.PackFixedBytes(ip.IP.To16())
        p.PackShort(ip.Port)


    def UnpackIP(p):
        ip = p.UnpackFixedBytes(16)
        port = p.UnpackShort()
        return IPDesc(IP=ip,Port=port)
    

    def PackIPs(p, ips):
        p.PackInt(int(len(ips)))
        i = 0
        while i < len(ips) and not p.Errored():
            p.PackIP(ips[i])
            i += 1
    

    def UnpackIPs(p):
        sliceSize = p.UnpackInt()
        ips = []
        i = int(0)
        if i < sliceSize and not p.Errored():
            ips = append(ips, p.UnpackIP())
            i += 1
        return ips
    

    def TryPackByte(packer, valIntf):
        val, ok = int(valIntf)
        if ok:
            packer.PackByte(val)
        else:
            packer.Add(Packer.errBadType)
    


    def TryUnpackByte(packer):
        return packer.UnpackByte()
    


    def TryPackShort(packer, valIntf):
        val, ok = int(valIntf)
        if ok:
            packer.PackShort(val)
        else:
            packer.Add(Packer.errBadType)
    

    def TryUnpackShort(packer):
        return packer.UnpackShort()


    def TryPackInt(packer, valIntf):
        val, ok = valIntf
        if ok:
            packer.PackInt(val)
        else:
            packer.Add(Packer.errBadType)
        


    def TryUnpackInt(packer):
        return packer.UnpackInt()
    

    def TryPackLong(packer, valIntf):
        val, ok = valIntf
        if ok:
            packer.PackLong(val)
        else:
            packer.Add(Packer.errBadType)
    

    def TryUnpackLong(packer):
        return packer.UnpackLong()


    def TryPackHash(packer, valIntf):
        val, ok = valIntf
        if ok:
            packer.PackFixedBytes(val)
        else:
            packer.Add(Packer.errBadType)


    def TryUnpackHash(packer):
        return packer.UnpackFixedBytes(hashing.HashLen)


    def TryPackHashes(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackFixedByteSlices(val)
        else:
            packer.Add(Packer.errBadType)


    def TryUnpackHashes(packer):
        return packer.UnpackFixedByteSlices(hashing.HashLen)


    def TryPackAddr(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackFixedBytes(val)
        else:
            packer.Add(Packer.errBadType)


    def TryUnpackAddr(packer):
        return packer.UnpackFixedBytes(hashing.AddrLen)
    

    def TryPackAddrList(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackFixedByteSlices(val)
        else:
            packer.Add(Packer.errBadType)


    def TryUnpackAddrList(packer):
        return packer.UnpackFixedByteSlices(hashing.AddrLen)
    

    def TryPackBytes(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackBytes(val)
        else:
            packer.Add(errBadType)


    def TryUnpackBytes(packer):
        return packer.UnpackBytes()


    def TryPack2DBytes(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.Pack2DByteSlice(val)
        else:
            packer.Add(errBadType)


    def TryUnpack2DBytes(packer):
        return packer.Unpack2DByteSlice()


    def TryPackStr(packer, valIntf):
        val, ok = valIntf(string)
        if ok:
            packer.PackStr(val)
        else:
            packer.Add(errBadType)


    def TryUnpackStr(packer):
        return packer.UnpackStr()



    def TryPackIP(packer, valIntf):
        val, ok = valIntf(IPDesc)
        if ok:
            packer.PackIP(val)
        else:
            packer.Add(errBadType)


    def TryUnpackIP(packer):
        return packer.UnpackIP()


    def TryPackIPList(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackIPs(val)
        else:
            packer.Add(errBadType)


    def TryUnpackIPList(packer):
        return packer.UnpackIPs()
    

    def Errored(packer):
        return len(packer.Errs) > 0


    def Add(packer, errors):
        for e in errors:
            packer.Errs.append(e)


    def Bytes(self):
        return self.Bytes

        