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


from avaxpython.utils import nlimits

class Packer:

    # MaxStringLen ...
    MaxStringLen = nlimits.limits(nlimits.c_uint16)[1]

    # ByteLen is the number of bytes per byte...
    ByteLen = 1
    # ShortLen is the number of bytes per short
    ShortLen = 2
    # IntLen is the number of bytes per int
    IntLen = 4
    # LongLen is the number of bytes per long
    LongLen = 8
    # BoolLen is the number of bytes per bool
    BoolLen = 1

    errBadLength = Exception("packer has insufficient length for input")
    errNegativeOffset = Exception("negative offset")
    errInvalidInput = Exception("input does not match expected format")
    errBadType = Exception("wrong type passed")
    errBadBool = Exception("unexpected value when unpacking bool")

    Errs = []

    # The largest allowed size of expanding the byte array
    MaxSize = 0
    # The current byte array
    Bytes = []
    # The offset that is being written to in the byte array
    Offset = 0

    # CheckSpace requires that there is at least [bytes] of write space left in the
    # byte array. If this is not true, an error is added to the packer
    @staticmethod
    def CheckSpace(bytes):
        
        if p.Offset < 0:
            p.Add(errNegativeOffset)
        if bytes < 0:
            p.Add(errInvalidInput)
        if len(p.Bytes)-p.Offset < bytes:
            p.Add(errBadLength)
        

    # Expand ensures that there is [bytes] bytes left of space in the byte slice.
    # If this is not allowed due to the maximum size, an error is added to the packer
    # In order to understand this code, its important to understand the difference
    # between a slice's length and its capacity.    
    @staticmethod
    def Expand(bytes):
        neededSize = bytes + p.Offset # Need byte slice's length to be at least [neededSize]
        
        if neededSize <= len(p.Bytes): # Byte slice has sufficient length already
            return
        elif neededSize > p.MaxSize: # Lengthening the byte slice would cause it to grow too large
            p.Err = errBadLength
            return
        elif neededSize <= cap(p.Bytes): # Byte slice has sufficient capacity to lengthen it without mem alloc
            p.Bytes = p.Bytes[:neededSize]
            return
        else: # Add capacity/length to byte slice
            p.Bytes = append(p.Bytes[:cap(p.Bytes)], [])
        
    

    # PackByte append a byte to the byte array
    @staticmethod
    def PackByte(val):
        p.Expand(ByteLen)
        if p.Errored():
            return

        p.Bytes[p.Offset] = val
        p.Offset += 1

    # UnpackByte unpack a byte from the byte array
    @staticmethod
    def UnpackByte():
        p.CheckSpace(ByteLen)
        if p.Errored():
            return 0        

        val = p.Bytes[p.Offset]
        p.Offset += 1
        return val    

    # PackShort append a short to the byte array
    @staticmethod
    def PackShort(val):
        p.Expand(ShortLen)
        if p.Errored():
            return

        binary.BigEndian.PutUint16(p.Bytes[p.Offset:], val)
        p.Offset += ShortLen

    # UnpackShort unpack a short from the byte array
    @staticmethod
    def UnpackShort():
        p.CheckSpace(ShortLen)
        if p.Errored():
            return 0        

        val = binary.BigEndian.Uint16(p.Bytes[p.Offset:])
        p.Offset += ShortLen
        return val

    # PackInt append an int to the byte array
    @staticmethod
    def PackInt(val):
        p.Expand(IntLen)
        if p.Errored():
            return

        binary.BigEndian.PutUint32(p.Bytes[p.Offset:], val)
        p.Offset += IntLen

    # UnpackInt unpack an int from the byte array
    @staticmethod
    def UnpackInt():
        p.CheckSpace(IntLen)
        if p.Errored():
            return 0

        val = binary.BigEndian.Uint32(p.Bytes[p.Offset:])
        p.Offset += IntLen
        return val

    # PackLong append a long to the byte array
    @staticmethod
    def PackLong(val):
        p.Expand(LongLen)
        if p.Errored():
            return

        binary.BigEndian.PutUint64(p.Bytes[p.Offset:], val)
        p.Offset += LongLen

    # UnpackLong unpack a long from the byte array
    @staticmethod
    def UnpackLong():
        p.CheckSpace(LongLen)
        if p.Errored():
            return 0
        
        val = binary.BigEndian.Uint64(p.Bytes[p.Offset:])
        p.Offset += LongLen
        return val
    

    # PackBool packs a bool into the byte array
    @staticmethod
    def PackBool(b):
        if b:
            p.PackByte(1)
        else:
            p.PackByte(0)
        

    # UnpackBool unpacks a bool from the byte array
    @staticmethod
    def UnpackBool():
        b = p.UnpackByte()
        
        if b == 0:
            return false
        elif b == 1:
            return true
        else:
            p.Add(errBadBool)
            return false
    

    # PackFixedBytes append a byte slice, with no length descriptor to the byte
    # array
    @staticmethod
    def PackFixedBytes(bytes):
        p.Expand(len(bytes))
        if p.Errored():
            return

        copy(p.Bytes[p.Offset:], bytes)
        p.Offset += len(bytes)

    # UnpackFixedBytes unpack a byte slice, with no length descriptor from the byte
    # array
    @staticmethod
    def UnpackFixedBytes(size):
        p.CheckSpace(size)
        if p.Errored():
            return nil

        bytes = p.Bytes[p.Offset : p.Offset+size]
        p.Offset += size
        return bytes


    # PackBytes append a byte slice to the byte array
    @staticmethod
    def PackBytes(bytes):
        p.PackInt(uint32(len(bytes)))
        p.PackFixedBytes(bytes)

    # UnpackBytes unpack a byte slice from the byte array
    @staticmethod
    def UnpackBytes():
        size = p.UnpackInt()
        return p.UnpackFixedBytes(int(size))

    # PackFixedByteSlices append a byte slice slice to the byte array
    @staticmethod
    def PackFixedByteSlices(byteSlices):
        p.PackInt(uint32(len(byteSlices)))
        for _, bytes in byteSlices:
            p.PackFixedBytes(bytes)

    # UnpackFixedByteSlices returns a byte slice slice from the byte array.
    # Each byte slice has the specified size. The number of byte slices is
    # read from the byte array.
    @staticmethod
    def UnpackFixedByteSlices(size):
        sliceSize = p.UnpackInt()
        bytes =(nil)
        i = uint32(0)
        while i < sliceSize and not p.Errored():
            bytes = append(bytes, p.UnpackFixedBytes(size))
            i += 1
        
        return bytes
    

    # Pack2DByteSlice append a 2D byte slice to the byte array
    @staticmethod
    def Pack2DByteSlice(byteSlices):
        p.PackInt(uint32(len(byteSlices)))
        for _, bytes in byteSlices:
            p.PackBytes(bytes)

    # Unpack2DByteSlice returns a 2D byte slice from the byte array.
    @staticmethod
    def Unpack2DByteSlice():
        sliceSize = p.UnpackInt()
        bytes =(nil)
        i = uint32(0)
        while i < sliceSize and not p.Errored():
            bytes = append(bytes, p.UnpackBytes())
            i += 1

        return bytes

    # PackStr append a string to the byte array
    @staticmethod
    def PackStr(str):
        strSize = len(str)
        if strSize > MaxStringLen:
            p.Add(errInvalidInput)

        p.PackShort(uint16(strSize))
        p.PackFixedBytes([])


    # UnpackStr unpacks a string from the byte array
    @staticmethod
    def UnpackStr():
        strSize = p.UnpackShort()
        return string(p.UnpackFixedBytes(int(strSize)))

    # PackIP packs an ip port pair to the byte array
    @staticmethod
    def PackIP(ip):
        p.PackFixedBytes(ip.IP.To16())
        p.PackShort(ip.Port)


    # UnpackIP unpacks an ip port pair from the byte array
    @staticmethod
    def UnpackIP():
        ip = p.UnpackFixedBytes(16)
        port = p.UnpackShort()
        return utils.IPDesc(IP=ip,Port=port)
    

    # PackIPs unpacks an ip port pair slice from the byte array
    @staticmethod
    def PackIPs(ips):
        p.PackInt(uint32(len(ips)))
        i = 0
        while i < len(ips) and not p.Errored():
            p.PackIP(ips[i])
            i += 1
    

    # UnpackIPs unpacks an ip port pair slice from the byte array
    @staticmethod
    def UnpackIPs():
        sliceSize = p.UnpackInt()
        ips = []
        i = uint32(0)
        if i < sliceSize and not p.Errored():
            ips = append(ips, p.UnpackIP())
            i += 1
        return ips
    

    # TryPackByte attempts to pack the value as a byte
    @staticmethod
    def TryPackByte(packer, valIntf):
        val, ok = int(valIntf)
        if ok:
            packer.PackByte(val)
        else:
            packer.Add(errBadType)
    

    # TryUnpackByte attempts to unpack a value as a byte
    @staticmethod
    def TryUnpackByte(packer):
        return packer.UnpackByte()
    

    # TryPackShort attempts to pack the value as a short
    @staticmethod
    def TryPackShort(packer, valIntf):
        val, ok = int(valIntf)
        if ok:
            packer.PackShort(val)
        else:
            packer.Add(errBadType)
    

    # TryUnpackShort attempts to unpack a value as a short
    @staticmethod
    def TryUnpackShort(packer):
        return packer.UnpackShort()


    # TryPackInt attempts to pack the value as an int
    @staticmethod
    def TryPackInt(packer, valIntf):
        val, ok = valIntf
        if ok:
            packer.PackInt(val)
        else:
            packer.Add(errBadType)
        

    # TryUnpackInt attempts to unpack a value as an int
    @staticmethod
    def TryUnpackInt(packer):
        return packer.UnpackInt()
    

    # TryPackLong attempts to pack the value as a long
    @staticmethod
    def TryPackLong(packer, valIntf):
        val, ok = valIntf
        if ok:
            packer.PackLong(val)
        else:
            packer.Add(errBadType)
    

    # TryUnpackLong attempts to unpack a value as a long
    @staticmethod
    def TryUnpackLong(packer):
        return packer.UnpackLong()


    # TryPackHash attempts to pack the value as a 32-byte sequence
    @staticmethod
    def TryPackHash(packer, valIntf):
        val, ok = valIntf
        if ok:
            packer.PackFixedBytes(val)
        else:
            packer.Add(errBadType)


    # TryUnpackHash attempts to unpack the value as a 32-byte sequence
    @staticmethod
    def TryUnpackHash(packer):
        return packer.UnpackFixedBytes(hashing.HashLen)


    # TryPackHashes attempts to pack the value as a list of 32-byte sequences
    @staticmethod
    def TryPackHashes(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackFixedByteSlices(val)
        else:
            packer.Add(errBadType)


    # TryUnpackHashes attempts to unpack the value as a list of 32-byte sequences
    @staticmethod
    def TryUnpackHashes(packer):
        return packer.UnpackFixedByteSlices(hashing.HashLen)


    # TryPackAddr attempts to pack the value as a 20-byte sequence
    @staticmethod
    def TryPackAddr(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackFixedBytes(val)
        else:
            packer.Add(errBadType)


    # TryUnpackAddr attempts to unpack the value as a 20-byte sequence
    @staticmethod
    def TryUnpackAddr(packer):
        return packer.UnpackFixedBytes(hashing.AddrLen)
    

    # TryPackAddrList attempts to pack the value as a list of 20-byte sequences
    @staticmethod
    def TryPackAddrList(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackFixedByteSlices(val)
        else:
            packer.Add(errBadType)


    # TryUnpackAddrList attempts to unpack the value as a list of 20-byte sequences
    @staticmethod
    def TryUnpackAddrList(packer):
        return packer.UnpackFixedByteSlices(hashing.AddrLen)
    

    # TryPackBytes attempts to pack the value as a list of bytes
    @staticmethod
    def TryPackBytes(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackBytes(val)
        else:
            packer.Add(errBadType)

    # TryUnpackBytes attempts to unpack the value as a list of bytes
    @staticmethod
    def TryUnpackBytes(packer):
        return packer.UnpackBytes()


    # TryPack2DBytes attempts to pack the value as a 2D byte slice
    @staticmethod
    def TryPack2DBytes(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.Pack2DByteSlice(val)
        else:
            packer.Add(errBadType)

    # TryUnpack2DBytes attempts to unpack the value as a 2D byte slice
    @staticmethod
    def TryUnpack2DBytes(packer):
        return packer.Unpack2DByteSlice()


    # TryPackStr attempts to pack the value as a string
    @staticmethod
    def TryPackStr(packer, valIntf):
        val, ok = valIntf(string)
        if ok:
            packer.PackStr(val)
        else:
            packer.Add(errBadType)


    # TryUnpackStr attempts to unpack the value as a string
    @staticmethod
    def TryUnpackStr(packer):
        return packer.UnpackStr()


    # TryPackIP attempts to pack the value as an ip port pair
    @staticmethod
    def TryPackIP(packer, valIntf):
        val, ok = valIntf(utils.IPDesc)
        if ok:
            packer.PackIP(val)
        else:
            packer.Add(errBadType)


    # TryUnpackIP attempts to unpack the value as an ip port pair
    @staticmethod
    def TryUnpackIP(packer):
        return packer.UnpackIP()


    # TryPackIPList attempts to pack the value as an ip port pair list
    @staticmethod
    def TryPackIPList(packer, valIntf):
        val, ok = valIntf([])
        if ok:
            packer.PackIPs(val)
        else:
            packer.Add(errBadType)


    # TryUnpackIPList attempts to unpack the value as an ip port pair list
    @staticmethod
    def TryUnpackIPList(packer):
        return packer.UnpackIPs()
    
