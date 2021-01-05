# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

# Python C language limits, from https://stackoverflow.com/questions/52475749/maximum-and-minimum-value-of-c-types-integers-from-python

import sys

from ctypes import c_int8, c_uint8, c_byte, c_ubyte, c_int16, c_uint16, \
    c_int32, c_uint32, c_int, c_uint, c_long, c_ulong, c_longlong, c_ulonglong, \
    c_int64, c_uint64, \
    sizeof

def limits(c_int_type):
    signed = c_int_type(-1).value < c_int_type(0).value
    bit_size = sizeof(c_int_type) * 8
    signed_limit = 2 ** (bit_size - 1)
    return (-signed_limit, signed_limit - 1) if signed else (0, 2 * signed_limit - 1)

