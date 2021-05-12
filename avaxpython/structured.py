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


class AvaxStructured:
    """Utility class to generate __repr__ according to serialized field tags."""

    def __struct__(self):
        """
            __struct__() should provide a JSON-friendly Python representation of an object tree
            All AvaxStructured objects automatically inherit this general implementation, but are
            encouraged to provide their own for more fine grained representation.

            __struct__ does not return JSON. It simply structures Python objects into JSON-compatible types.
            That way the structure can be encoded in other formats if necessary.
        """
        _d = {}
        for field_key, field_dict in self._avax_tags:
            attr = getattr(self, field_key)
            j_key = field_key
            if "json" in field_dict and len(field_dict["json"]) > 0:
                j_key = field_dict["json"]
            if "__struct__" in dir(attr):
                _d[j_key] = attr.__struct__()
            else:
                _d[j_key] = attr

        return _d

    def __repr__(self):
        return str(self.__struct__())

