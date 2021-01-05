# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: @ojrdev @ https://crypto.bi
# --#--#--

# An Avalanche ID is defined as
# type ID [32]byte in avalanchego/ids/id.go



class ID:    

    __avax_id_length = 32

    def __init__(self):
        self.bytes = bytearray([0] * ID.__avax_id_length)