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

from avaxpython.types import *
from avaxpython.ids.ID import ID
from avaxpython.snow.choices.status import Status

class State:
	_avax_interface = True
	# In [db], add a key-value pair.
	# [value] will be converted to bytes by calling Bytes() on it.
	# [typeID] must have already been registered using RegisterType.
	# If [value] is nil, the value associated with [key] and [typeID] is deleted (if it exists).
	def Put(self, db, typeID: Uint64, key: ID, value):
		pass

	# From [db], get the value of type [typeID] whose key is [key]
	# Returns database.ErrNotFound if the entry doesn't exist
	def Get(self, db, typeID: Uint64, key: ID):
		pass

	# Return whether [key] exists in [db] for type [typeID]
	def Has(self, db, typeID: Uint64, key: ID):
		pass

	# PutStatus associates [key] with [status] in [db]
	def PutStatus(self, db, key: ID, status: Status):
		pass

	# GetStatus gets the status associated with [key] in [db]
	def GetStatus(self, db, key: ID) -> Status:
		pass

	# PutID associates [key] with [ID] in [db]
	def PutID(self, db, key: ID, ID: ID):
		pass

	# GetID gets the ID associated with [key] in [db]
	def GetID(self, db, key: ID):
		pass

	# PutTime associates [key] with [time] in [db]
	def PutTime(self, db, key: ID, time):
		pass

	# GetTime gets the time associated with [key] in [db]
	def GetTime(self, db, key: ID):
		pass

	# Register a new type.
	# When values that were Put with [typeID] are retrieved from the database,
	# they will be unmarshaled from bytes using [unmarshal].
	# Returns an error if there is already a type with ID [typeID]
	def RegisterType(self, typeID: Uint64, marshal):
		pass


class state:
	def __init__(self):
		# Keys:   Type ID
		# Values: Function that unmarshals values
		#         that were Put with that type ID
		self.unmarshallers = {}

		# Keys:   Type ID
		# Values: Function that marshals values
		#         that were Put with that type ID
		self.marshallers  = {}

		# Keys:   Type ID
		# Values: Cache that stores uniqueIDs for values that were put with that type ID
		#         (Saves us from having to re-compute uniqueIDs)
		self.uniqueIDCaches  = {}

