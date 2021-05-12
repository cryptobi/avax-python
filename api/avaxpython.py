# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Support this Open Source project!
Donate to X-avax1qr6yzjykcjmeflztsgv6y88dl0xnlel3chs3r4

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


import avaxconfig
import jsrpc
import inspect
from apimeta import api_meta

def make_caller(url):

    def f(method, data):
        return jsrpc.ava_call(url, method, data)    

    return f


def make_poster(url):

    def f(data):
        return jsrpc.ava_post(url, data)    

    return f


def get_caller():
    """
    Uses the source caller's module name to determine
    which caller to return. 
    Will fail if source is __main__. Do not call module
    functions directly from command line.
    """
    src_caller = inspect.stack()[1]
    module_name = inspect.getmodule(src_caller[0]).__name__ 
    return make_caller(avaxconfig.urls[module_name])


def get_poster():
    src_caller = inspect.stack()[1]
    module_name = inspect.getmodule(src_caller[0])    
    return make_poster(avaxconfig.urls[module_name])
