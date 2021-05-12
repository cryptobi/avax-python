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


import ipaddress
from avaxpython.errors import errors

errBadIP = Exception("bad ip format")
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
	host, portStr = net.SplitHostPort(str)
	
	port = int(portStr)	
	ip = net.ParseIP(host)

	if ip == nil:
		return IPDesc(), errBadIP
	
	return IPDesc(IP=ip,Port=port), None


class IPDesc:

	V4 = 4
	V6 = 16

	def __init__(self, IP: str = "", Port: int = 0, Version = V4):
		self.IP = IP
		self.Port = Port
		self.version = Version

	def To16(self) -> bytes:
		ipaddr = ipaddress.ip_address(self.IP)
		pkt = ipaddr.packed
		if len(pkt) == 4:
			bts = bytearray([0] * 12)
			bts.extend(pkt)
			return bytes(bts)
		elif len(pkt) == 16:
			return pkt
		else:
			raise Exception(f"Unknown IP format {self.IP} binary {pkt}")


	def __str__(self):
		return f"{self.IP}:{self.Port}"


	def __repr__(self):
		return f"{self.IP}:{self.Port}"

	def Equal(self, other):
		return self.Port == other.Port and	self.IP.Equal(other.IP)	

	def PortString(self):
		return ":{}".format(self.Port)
	

	def String(self):
		return net.JoinHostPort(self.IP.String(), fmt.Sprintf("%d", self.Port))	

	def IsPrivate(self):
		"""	IsPrivate attempts to decide if the ip address in this descriptor is a local ip address.
		This function was taken from: https://stackoverflow.com/a/50825191/3478466
		"""
		ip = self.IP
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
		super().__init__()
		self.IPDesc = ipdesc		


class DynamicIPDesc(IPDescContainer):
	
	def __init__(self, ip, port):
		ipd = IPDesc(ip, port)
		self.IPDescContainer = IPDescContainer(ipd)
		self.IPDesc = ipd

	def __str__(self):
		return str(self.IPDesc)


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


