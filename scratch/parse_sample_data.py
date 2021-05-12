#!/usr/bin/python3
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


import os
import os.path
from avaxpython.network.codec import Codec


if "AVAX_PYTHON_PATH" not in os.environ:
    print("Please set AVAX_PYTHON_PATH environment variable. Run . setenv.sh")
    exit(1)

data_dir = "{}/sample-data".format(os.environ['AVAX_PYTHON_PATH'])


if not os.path.exists(data_dir):
    print("Directory {} does not exist. Create it first.".format(data_dir))
    exit(1)


for arr in os.walk(data_dir):
    for fil in arr[2]:
        path = "{}/{}".format(arr[0], fil)
        with open(path, "rb") as f:
            message = f.read()
            parsed_msg = Codec.Parse(message)
            print(parsed_msg)
