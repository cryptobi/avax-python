# Scripts for AVA API
# Author: https://github.com/zefonseca/
# License MIT

import socket
import sys
import platform
import ipc

# Export all blockchains
blockchains = platform.getBlockchains()

for bc in blockchains["blockchains"]:
    print(bc)
    id = bc["id"]
    ret = ipc.publishBlockchain(id)
    print(ret)


sys.exit()
# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = sys.argv[1]
print ('connecting to {}'.format(server_address))

sock.connect(server_address)

data = sock.recv(16)
amount_received = len(data)

while amount_received > 0:
    data = sock.recv(16)
    amount_received = len(data)
    print('received "{}"'.format(data))

