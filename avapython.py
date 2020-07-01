# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc
import inspect

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
    return make_caller(avaconfig.urls[module_name])


def get_poster():
    src_caller = inspect.stack()[1]
    module_name = inspect.getmodule(src_caller[0])    
    return make_poster(avaconfig.urls[module_name])    