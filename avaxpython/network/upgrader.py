
# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Documentation at https://crypto.bi

"""

Copyright © 2021 ojrdev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# --#--#--


from avaxpython.errors import errors

errNoCert = errors.New("tls handshake finished with no peer certificate")


# Upgrader interface
class Upgrader:

    def __init__(self):
        pass

    def Upgrade(conn):
        return conn


class ipUpgrader(Upgrader):
    def __init__(self):
        pass

    def Upgrade(conn):
        addr = conn.RemoteAddr()
        str = addr.String()
        id = ids.ShortID(hashing.ComputeHash160Array(bytearray(str)))
        return id, conn, nil


class tlsServerUpgrader(Upgrader):

    def __init__(self, tconfig):
        self.config = tconfig

    def Upgrade(self, conn):

        encConn = tls.Server(conn, t.config)
        err = encConn.Handshake()
        if err != nil:
            return ids.ShortID(), nil, err        

        connState = encConn.ConnectionState()
        if len(connState.PeerCertificates) == 0:
            return ids.ShortID(), nil, errNoCert
        
        peerCert = connState.PeerCertificates[0]
        id = ids.ShortID(hashing.ComputeHash160Array(hashing.ComputeHash256(peerCert.Raw)))
        return id, encConn, nil    


class tlsClientUpgrader(Upgrader):

    def __init__(self, tconfig):
        self.config = tconfig


    def Upgrade(self, conn):
        encConn = tls.Client(conn, t.config)
        err = encConn.Handshake()
        if err != nil:
            return ids.ShortID(), nil, err
        

        connState = encConn.ConnectionState()
        if len(connState.PeerCertificates) == 0:
            return ids.ShortID(), nil, errNoCert
        
        peerCert = connState.PeerCertificates[0]
        id = ids.ShortID(hashing.ComputeHash160Array(hashing.ComputeHash256(peerCert.Raw)))

        return id, encConn, nil
    

def NewIPUpgrader(): 
    return ipUpgrader()

def NewTLSServerUpgrader(config):
	return tlsServerUpgrader(config)

def NewTLSClientUpgrader(config):
	return tlsClientUpgrader(config)
