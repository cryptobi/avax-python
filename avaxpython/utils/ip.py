
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


import ipaddress
from avaxpython.errors import errors

errBadIP = errors.New("bad ip format")
# This was taken from: https://stackoverflow.com/a/50825191/3478466
privateIPBlocks = []

__cidrs = [
"127.0.0.0/8",    # IPv4 loopback
"10.0.0.0/8",     # RFC1918
"172.16.0.0/12",  # RFC1918
"192.168.0.0/16", # RFC1918
"169.254.0.0/16", # RFC3927 link-local
"::1/128",        # IPv6 loopback
"fe80::/10",      # IPv6 link-local
"fc00::/7",       # IPv6 unique local addr
]


def init():
	for cidr in __cidrs:
		block = IPNetwork(cidr)
		privateIPBlocks.append(block)


def ToIPDesc(ip_string):
	host, portStr, err = net.SplitHostPort(str)
	if err != nil:
		return IPDesc(), errBadIP
	
	port = int(portStr)	
	ip = net.ParseIP(host)

	if ip == nil:
		return IPDesc(), errBadIP
	
	return IPDesc(IP=ip,Port=port), None


class IPDesc:

	def __init__(self, ip, pt):
		self.addr = ipaddress.ip_address(ip)
		self.port = pt
		


class IPDesc:

	def __init__(self, IP, Port):
		self.IP = IP
		self.Port = Port


	def __repr__(self):
		return f"{self.IP}:{self.Port}"

	# Equal ...
	def Equal(otherIPDesc):
		return ipDesc.Port == otherIPDesc.Port and	ipDesc.IP.Equal(otherIPDesc.IP)	

	# PortString ...
	def PortString():
		return ":{}".format(self.Port)
	

	def String():
		return net.JoinHostPort(ipDesc.IP.String(), fmt.Sprintf("%d", ipDesc.Port))	

	# IsPrivate attempts to decide if the ip address in this descriptor is a local
	# ip address.
	# This function was taken from: https://stackoverflow.com/a/50825191/3478466
	def IsPrivate():
		ip = ipDesc.IP
		if ip.IsLoopback() or ip.IsLinkLocalUnicast() or ip.IsLinkLocalMulticast():
			return True

		for block in privateIPBlocks:
			if block.Contains(ip):
				return True
					
		return false
	
	# IsZero returns if the IP or port is zeroed out
	def IsZero(self):
		ip = self.IP
		return self.Port == 0 or len(ip) == 0 or ip == "0.0.0.0" # or ip.Equal(net.IPv6zero)
	

class IPDescContainer(IPDesc):

	def __init__(self, ipdesc):	
		self.IPDesc = ipdesc		


class DynamicIPDesc(IPDescContainer):
	
	def __init__(self, ip, port):
		ipd = IPDesc(ip, port)
		self.IPDescContainer = IPDescContainer(ipd)
		self.IPDesc = ipd

	def __repr__(self):
		return str(self.IPDesc)

	def IP(self):						
		return self.IPDesc

	def Update(self, ip: IPDesc):
		self.IPDesc = ip

	def UpdatePort(self, port: int):				
		self.IPDesc.Port = port


	def UpdateIP(self, ip):				
		i.IPDesc.IP = ip


def NewDynamicIPDesc(ip, port: int) -> DynamicIPDesc:
	return DynamicIPDesc(IPDescContainer = IPDescContainer(IPDesc = IPDesc(IP = ip, Port = port)))


