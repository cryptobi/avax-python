# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import avaconfig
import jsrpc


def metrics():
    mts = jsrpc.ava_post(avaconfig.murl, None).text
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
