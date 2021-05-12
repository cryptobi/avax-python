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



class Message:

    def __init__(self, messageType=None, validatorID=None, requestID=None, containerID=None, container: bytes=None,
                 containers=[], containerIDs=[], notification=None, received=None, deadline=None):
        self.messageType=messageType
        self.validatorID=validatorID
        self.requestID=requestID
        self.containerID=containerID
        self.container=container
        self.containers=containers
        self.containerIDs=containerIDs
        self.notification=notification
        self.received=received
        self.deadline=deadline

    def __repr__(self):
        c_count = 0
        if self.containers:
            try:
                c_count = len(self.containers)
            except Exception as _:
                c_count = 0
            
        _d = {
            "messageType": self.messageType,
            "validatorID": self.validatorID,
            "requestID": self.requestID,
            "containerID": self.containerID,
            "container": f"[BINARY] {len(self.container)} Bytes",
            "containers": f"[BINARY] {c_count} Containers",
            "containerIDs": self.containerIDs,
            "notification": self.notification,
            "received": self.received,
            "deadline": self.deadline            
        }
        return str(_d)