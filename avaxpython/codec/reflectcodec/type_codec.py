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

from numpy.core.fromnumeric import trace
from avaxpython.types import *
from avaxpython.codec.reflectcodec.struct_fielder import StructFielder
from avaxpython.utils.wrappers.Packer import Packer

errMarshalNil   = Exception("can't marshal undefined pointer or interface")
errUnmarshalNil = Exception("can't unmarshal undefined value")
errNeedPointer  = Exception("argument to unmarshal must be a pointer")
errExtraSpace   = Exception("trailing buffer space")

DefaultTagName = "serialize"
VersionTagName = "serializeV0"

class TypeCodec:
	
    def UnpackPrefix(packer, reflect_type):
        """UnpackPrefix unpacks the prefix of an interface from the given packer. The prefix specifies the concrete type that the interface should be deserialized into. This function returns a new instance of that concrete type. The concrete type must implement the given type.""" 
        pass

    def PackPrefix(packer, reflect_type):
        """ PackPrefix packs the prefix for the given type into the given packer. This identifies the bytes that follow, which are the byte representation of an interface, as having the given concrete type. When deserializing the bytes, the prefix specifies which concrete type to deserialize into."""
        pass


class genericCodec:
	""" genericCodec handles marshaling and unmarshaling of structs with a generic
		implementation for interface encoding.

		A few notes:
		1) We use "marshal" and "serialize" interchangeably, and "unmarshal" and "deserialize" interchangeably
		2) To include a field of a struct in the serialized form, add the tag `{tagName}:"true"` to it. `{tagName}` defaults to `serialize`.
		3) These typed members of a struct may be serialized:
		bool, string, int[8,16,32,64], int[8,16,32,64],
			structs, slices, arrays, interface.
			structs, slices and arrays can only be serialized if their constituent values can be.
		4) To marshal an interface, you must pass a pointer to the value
		5) To unmarshal an interface,  you must call codec.RegisterType([instance of the type that fulfills the interface]).
		6) Serialized fields must be exported
		7) Undefined slice variables are marshaled as empty slices"""

	def __init__(self, typer, tagName, maxSliceLen):

		self.typer: TypeCodec = typer
		self.maxSliceLen:int = maxSliceLen
		self.fielder: StructFielder


	@classmethod
	def Unmarshal(cls, bbytes: bytes, dest, element_type=None, type_ids={}, seq=[]):
		"""
		Unmarshal unmarshals [bytes] into an instance of dest, where [dest] must either be a type
		listed on avaxpython.types or a reference type containing _avax_tags.

		Parameters:
		cls : The codec class to use, defaults to this class.
		bbytes: Raw bytes to deserialize
		dest: Destination element type.
		element_type: The type of elements when deserializing arrays. Ignored for non-array types.
		type_ids : Dict mapping type ID integers to classes.

		"""

		if dest == None:
			raise errUnmarshalNil

		p = Packer(bbytes)		

		dest = cls._unmarshal(p, dest, element_type, type_ids=type_ids, seq=[type(dest)])
		
		if p.Offset != len(bbytes):
			raise errExtraSpace

		return dest

	@classmethod
	def _unmarshal(cls, p: Packer, value, element_type=None, type_ids={}, seq=[]):		

		datatype = type(value)

		if datatype is Uint8:
			return p.UnpackByte()
		elif datatype is Int8:
			return p.UnpackByte()
		elif datatype is Uint16:
			return p.UnpackShort()
		elif datatype is Int16:
			return p.UnpackShort()
		elif datatype is Uint32:
			return p.UnpackInt()
		elif datatype is Int32:
			return p.UnpackInt()
		elif datatype is Uint64:
			return p.UnpackLong()
		elif datatype is Int64:
			return p.UnpackLong()
		elif datatype is Bool:
			return p.UnpackBool()			
		elif datatype is ByteSlices:
			ret = ByteSlices([])
			num_elements_32 = p.UnpackInt()

			if num_elements_32 > (1 << 32):
				raise IndexError(f"array length, {num_elements_32}, exceeds maximum length, {(1 << 32)}")

			num_elements = int(num_elements_32)
		
			# Unmarshal each element into the appropriate index of the slice
			for i in range(num_elements):
				item = p.UnpackBytes()
				ret.slices.append(item)

			return ret			

		elif datatype is ByteArrays:
			ret = ByteArrays(array_size=value.array_size)
			ret.arrays = []

			num_elements_32 = p.UnpackInt()

			if num_elements_32 > (1 << 32):
				raise IndexError(f"array length, {num_elements_32}, exceeds maximum length, {(1 << 32)}")

			num_elements = int(num_elements_32)
		
			# Unmarshal each element into the appropriate index of the slice
			for i in range(num_elements):
				item = p.UnpackFixedBytes(value.array_size)
				ret.arrays.append(item)

			return ret			


		elif datatype is Slice:
			ret = []
			num_elements_32 = p.UnpackInt()

			if num_elements_32 > (1 << 32):
				raise IndexError(f"array length, {num_elements_32}, exceeds maximum length, {(1 << 32)}")

			num_elements = int(num_elements_32)

			# If this is a slice of bytes, manually unpack the bytes rather
			# than calling unmarshal on each byte. This improves performance.						
			if datatype is bytes:
				return p.UnpackFixedBytes(num_elements)				
		
			# Unmarshal each element into the appropriate index of the slice
			for i in range(num_elements):

				if element_type is Array:
					item = cls._unmarshal(p, element_type(), type_ids=type_ids, seq=seq + [element_type])
				else:
					item = cls._unmarshal(p, element_type(), type_ids=type_ids, seq=seq + [element_type])

				ret.append(item)

			return ret				

		elif datatype is Bytes:
			
			num_elements_32 = len(value)

			if num_elements_32 > (1 << 32):
				raise IndexError(f"array length, {num_elements_32}, exceeds maximum length, {(1 << 32)}")

			# If this is a slice of bytes, manually unpack the bytes rather
			# than calling unmarshal on each byte. This improves performance.						
			
			return p.UnpackFixedBytes(num_elements_32)				


		elif datatype is Array:
			
			ret = []
			num_elements_32 = len(value)

			if num_elements_32 > (1 << 32):
				raise IndexError(f"array length, {num_elements_32}, exceeds maximum length, {(1 << 32)}")					

			# Unmarshal each element into the appropriate index of the slice
			for i in range(num_elements_32):
				item = cls._unmarshal(p, element_type(), type_ids = type_ids, seq=seq+[element_type])
				ret.append(item)

			return ret				

		elif datatype is String:
			return p.UnpackStr()
		elif "_avax_interface" in dir(datatype):

			type_id = p.UnpackInt() 			
			
			if type_id not in type_ids:
				raise TypeError(f"Interface {datatype} typeID {type_id} not mapped in type_ids. Cannot proceed.")

			concrete_type = type_ids[type_id]
			return cls._unmarshal(p, concrete_type(), None, type_ids = type_ids, seq=seq+[concrete_type])
			
		else:
			
			if "_avax_tags" not in dir(value):
				raise LookupError("Unmarshaling classes requires the _avax_tags attribute.")

			# Go through the fields and umarshal into them						
			for field_k, field_dict in value._avax_tags:
				
				do_ser = ((VersionTagName in field_dict) and field_dict[VersionTagName])
				do_ser = do_ser or ( (DefaultTagName in field_dict) and field_dict[DefaultTagName])

				if do_ser:					
					e_type = None
					if "element_type" in field_dict:
						e_type = field_dict["element_type"]
					field_value = cls._unmarshal(p, getattr(value, field_k), e_type, type_ids=type_ids, seq=seq+[type(getattr(value, field_k))])
					setattr(value, field_k, field_value)					

			return value				
			


