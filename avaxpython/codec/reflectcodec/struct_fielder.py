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

# SliceLenTagName that specifies the length of a slice.
SliceLenTagName = "len"

# TagValue is the value the tag must have to be serialized.
TagValue = "true"


class FieldDesc:
    def __init__(self, index:int, maxslice:int) -> None:        
        self.Index: int = index
        self.MaxSliceLen:int = maxslice


class StructFielder:
    """
    StructFielder handles discovery of serializable fields in a struct.
	Returns the fields that have been marked as serializable in [t], which is
	a struct type. Additionally, returns the custom maximum length slice that
	may be serialized into the field, if any.
	Returns an error if a field has tag "[tagName]: [TagValue]" but the field
	is un-exported.
	GetSerializedField(Foo) --> [1,5,8] means Foo.Field(1), Foo.Field(5),
	Foo.Field(8) are to be serialized/deserialized.
    """
    def __init__(self, tagname, maxslicelen) -> None:
        self.tagName = tagname
        self.maxSliceLen = maxslicelen
        # Key: a struct type
        # Value: Slice where each element is index in the struct type of a field
        # that is serialized/deserialized e.g. Foo --> [1,5,8] means Foo.Field(1),
        # etc. are to be serialized/deserialized. We assume this cache is pretty
        # small (a few hundred keys at most) and doesn't take up much memory.
        self.serializedFieldIndices = {} # map[reflect.Type][]FieldDesc
        
    def GetSerializedFields(self, t: type):
        pass    


    def GetSerializedFields(s, t : type):
        
        if t in s.serializedFieldIndices:
            return s.serializedFieldIndices[t]
        
        numFields = t.NumField()
        serializedFields = []
        for i in range(numFields):
            field = t.Field(i)
            if field.Tag.Get(s.tagName) != TagValue:
                continue
            
            if unicode.IsLower(rune(field.Name[0])):
                raise Exception(f"can't marshal un-exported field {field.Name}")
            
            sliceLenField = field.Tag.Get(SliceLenTagName)
            maxSliceLen = s.maxSliceLen

            newLen = strconv.ParseUint(sliceLenField, 10, 31)
            if newLen is None:
                maxSliceLen = int(newLen)
            
            serializedFields.append(FieldDesc(Index=i, MaxSliceLen=maxSliceLen))        
        
        s.serializedFieldIndices[t] = serializedFields # cache result
        return serializedFields
