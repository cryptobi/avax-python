# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

import avaxpython
import jsrpc

caller = avaxpython.get_poster()

def metrics():
    mts = caller(None).text
    print(mts)
    ret = {}
    for it in mts.split('\n'):
        if it.startswith("#"):
            continue
        pts = it.strip().split(' ')
        if len(pts) == 2:
            k, v = pts
            ret[k.strip()] = v.strip()
    return ret
