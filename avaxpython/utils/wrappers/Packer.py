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


import ipaddress
from asn1crypto.x509 import Certificate
from avaxpython.utils.ip import IPDesc
from avaxpython.utils.ipcert import IPCertDesc
from avaxpython.utils import nlimits
from avaxpython.utils.hashing import hashing
from avaxpython.types import *


class Packer:
    MaxStringLen = 65535
    ByteLen = 1
    ShortLen = 2
    IntLen = 4
    LongLen = 8
    BoolLen = 1

    error_bad_length = Exception("packer has insufficient length for input")
    error_negative_offset = Exception("negative offset")
    error_invalid_input = Exception("input does not match expected format")
    error_bad_type = Exception("wrong type passed")
    error_bad_bool = Exception("unexpected value when unpacking bool")

    def __init__(self, b: bytes):
        self.Bytes: bytes = b
        self.Offset = 0
        self.Errs = []

    def PackByte(self, val):

        if self.Errored():
            return

        barr = bytearray(self.Bytes)
        barr.extend(val.to_bytes(1, "big"))
        self.Bytes = Bytes(barr)
        self.Offset += 1

    def UnpackByte(self):

        if self.Errored():
            return 0

        endoff = self.Offset + 1
        val = self.Bytes[self.Offset:endoff]
        self.Offset += 1
        return Byte(val)

    def PackShort(self, val):
        if self.Errored():
            return

        barr = bytearray(self.Bytes)
        barr.extend(val.to_bytes(Packer.ShortLen, "big"))
        self.Bytes = bytes(barr)
        self.Offset += Packer.ShortLen

    def UnpackShort(self):
        if self.Errored():
            return 0

        endoff = self.Offset + Packer.ShortLen
        val = int.from_bytes(self.Bytes[self.Offset:endoff], "big")
        self.Offset += Packer.ShortLen
        return Uint16(val)

    def PackInt(self, val):
        if self.Errored():
            return

        barr = bytearray(self.Bytes)
        barr.extend(val.to_bytes(Packer.IntLen, "big"))
        self.Bytes = bytes(barr)

        self.Offset += Packer.IntLen

        return val

    def UnpackInt(self):
        if self.Errored():
            return 0

        endoff = self.Offset + Packer.IntLen
        val = int.from_bytes(self.Bytes[self.Offset:endoff], "big")
        self.Offset += Packer.IntLen
        return Uint32(val)

    def PackLong(self, val):
        if self.Errored():
            return

        barr = bytearray(self.Bytes)
        barr.extend(val.to_bytes(Packer.LongLen, "big"))
        self.Bytes = bytes(barr)
        self.Offset += Packer.LongLen

        return val

    def UnpackLong(self):
        if self.Errored():
            return 0

        endoff = self.Offset + Packer.LongLen
        val = int.from_bytes(self.Bytes[self.Offset:endoff], "big")
        self.Offset += Packer.LongLen
        return Uint64(val)

    def PackBool(self, b):
        if b:
            self.PackByte(1)
        else:
            self.PackByte(0)

    def UnpackBool(self):
        b = self.UnpackByte()

        if b == 0:
            return Bool(False)
        elif b == 1:
            return Bool(True)
        else:
            self.Add(f"Invalid bool {b}")
            return Bool(False)

    def PackFixedBytes(self, bbytes):
        if self.Errored():
            return

        barr = bytearray(self.Bytes)
        barr.extend(bbytes)
        self.Bytes = bytes(barr)
        self.Offset += len(bbytes)

    def UnpackFixedBytes(self, size: int):
        if self.Errored():
            return None

        bbytes = self.Bytes[self.Offset: self.Offset + size]
        self.Offset += size
        return Bytes(bbytes)

    def PackBytes(self, dbytes):
        self.PackInt(int(len(dbytes)))
        self.PackFixedBytes(dbytes)

    def UnpackBytes(self):
        size = self.UnpackInt()
        return self.UnpackFixedBytes(int(size))

    def PackFixedByteSlices(self, byte_slices):
        self.PackInt(len(byte_slices))
        for bbytes in byte_slices:
            self.PackFixedBytes(bbytes)

    def UnpackFixedByteSlices(self, size: int):
        sliceSize = self.UnpackInt()
        bbytes = []
        i = int(0)
        while i < sliceSize and not self.Errored():
            bts = self.UnpackFixedBytes(size)
            bbytes.append(bts)
            i += 1

        return Bytes(bbytes)

    def Pack2DByteSlice(self, byteSlices):
        self.PackInt(len(byteSlices))
        for bbytes in byteSlices:
            self.PackBytes(bbytes)

    def Unpack2DByteSlice(self):
        slice_size = self.UnpackInt()
        bbytes = []
        i = 0
        while i < slice_size and not self.Errored():
            bts = self.UnpackBytes()
            bbytes.append(bts)
            i += 1

        return Slice(bbytes)

    def PackStr(self, dstr):
        str_size = len(dstr)
        if str_size > Packer.MaxStringLen:
            self.Add(Packer.error_invalid_input)

        self.PackShort(str_size)
        self.PackFixedBytes(bytes(dstr, "utf-8"))

    def UnpackStr(self):
        strSize = self.UnpackShort()
        bts = self.UnpackFixedBytes(int(strSize))

        return String(bts.decode("utf-8"))

    def PackIP(self, ip: IPDesc):
        ipto16_a = ip.To16()

        barr = bytearray(ipto16_a)
        if ip.version == IPDesc.V4:
            barr[-6] = 0xff
            barr[-5] = 0xff

        ipto16 = bytes(barr)

        self.PackFixedBytes(ipto16)
        self.PackShort(ip.Port)

    def UnpackIP(self):
        ipbytes = self.UnpackFixedBytes(16)
        ipa = None
        if ipbytes[-6] == 0xff and ipbytes[-5] == 0xff:
            ipa = ipaddress.IPv4Address(ipbytes[-4:])            
        else:
            ipa = ipaddress.IPv6Address(ipbytes)            

        port = self.UnpackShort()
        return IPDesc(IP=str(ipa), Port=port)

    def PackIPs(self, ips):
        self.PackInt(len(ips))
        i = 0
        while i < len(ips) and not self.Errored():
            self.PackIP(ips[i])
            i += 1

    def UnpackIPs(self):
        sliceSize = self.UnpackInt()        
        ips = []
        i = 0
        while i < sliceSize and not self.Errored():
            ips.append(self.UnpackIP())
            i += 1

        return Slice(ips)

    def TryPackByte(self, valIntf):
        self.PackByte(valIntf)

    def TryUnpackByte(self):
        return self.UnpackByte()

    def TryPackShort(self, valIntf):
        self.PackShort(valIntf)

    def TryUnpackShort(self):
        return self.UnpackShort()

    def TryPackInt(self, valIntf):
        self.PackInt(valIntf)

    def TryUnpackInt(self):
        return self.UnpackInt()

    def TryPackLong(self, valIntf):
        self.PackLong(valIntf)

    def TryUnpackLong(self):
        return self.UnpackLong()

    def TryPackHash(self, valIntf):
        self.PackFixedBytes(valIntf)

    def TryUnpackHash(self):
        return self.UnpackFixedBytes(hashing.HashLen)

    def TryPackHashes(self, valIntf):
        self.PackFixedByteSlices(valIntf)

    def TryUnpackHashes(self):
        return self.UnpackFixedByteSlices(hashing.HashLen)

    def TryPackAddr(self, valIntf):
        self.PackFixedBytes(valIntf)

    def TryUnpackAddr(self):
        return self.UnpackFixedBytes(hashing.AddrLen)

    def TryPackAddrList(self, valIntf):
        self.PackFixedByteSlices(valIntf)

    def TryUnpackAddrList(self):
        return self.UnpackFixedByteSlices(hashing.AddrLen)

    def TryPackBytes(self, valIntf):
        self.PackBytes(valIntf)

    def TryUnpackBytes(self):
        return self.UnpackBytes()

    def TryPack2DBytes(self, valIntf):
        self.Pack2DByteSlice(valIntf)

    def TryUnpack2DBytes(self):
        return self.Unpack2DByteSlice()

    def TryPackStr(self, valIntf):
        self.PackStr(valIntf)

    def TryUnpackStr(self):
        return self.UnpackStr()

    def TryPackIP(self, valIntf):
        self.PackIP(valIntf)

    def TryUnpackIP(self):
        return self.UnpackIP()

    def TryPackIPList(self, valIntf):
        self.PackIPs(valIntf)

    def TryUnpackIPList(self):
        return self.UnpackIPs()

    def Errored(self):
        return len(self.Errs) > 0

    def Add(self, errors):
        for e in errors:
            self.Errs.append(e)

    def TryPackX509Certificate(self, valIntf):
        if isinstance(valIntf, Certificate):    
            self.PackX509Certificate(valIntf)
        else:
            self.Add(Packer.error_bad_type)

    def TryUnpackX509Certificate(self):
        return self.UnpackX509Certificate()

    def PackX509Certificate(self, cert: Certificate):        
        self.PackBytes(cert.dump())
    
    def UnpackX509Certificate(self) -> Certificate:
        b = self.UnpackBytes()
        if len(b) == 0:
            return None
                
        cert = Certificate.load(b)
        if cert is None:
            self.Add(Exception("Error Parsing X509 Cert"))            
            return None

        return cert    

    def TryPackIPCert(self, valIntf):
        if isinstance(valIntf, IPCertDesc):        
            self.PackIPCert(valIntf)
        else:
            self.Add(Packer.error_bad_type)        
    
    def TryUnpackIPCert(self):
        return self.UnpackIPCert()
    
    def PackIPCert(self, ipCert: IPCertDesc):
        self.PackX509Certificate(ipCert.Cert)
        self.PackIP(ipCert.IPDesc)
        self.PackLong(ipCert.Time)
        self.PackBytes(ipCert.Signature)
    
    def UnpackIPCert(self) -> IPCertDesc:
        ipCert = IPCertDesc()
        ipCert.Cert = self.UnpackX509Certificate()
        ipCert.IPDesc = self.UnpackIP()
        ipCert.Time = self.UnpackLong()
        ipCert.Signature = self.UnpackBytes()
        return ipCert    

    def TryPackIPCertList(self, valIntf):
        if isinstance(valIntf[0], IPCertDesc):        
            self.PackInt(Uint32(len(valIntf)))
            for ipc in IPCertDesc:
                self.PackIPCert(ipc)
        else:
            self.Add(Packer.error_bad_type)

    def TryUnpackIPCertList(self):
        slice_size = self.UnpackInt()
        ips = []
        for i in range(slice_size):
            ips.append(self.UnpackIPCert())

        return ips


