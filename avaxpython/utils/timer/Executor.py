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


from threading import Thread, Lock, Condition
from avaxpython.parallel.Parallel import Parallel

class Executor:

    def __init__(self):
        self.lock = Lock()
        self.cond = Condition(self.lock)
        self.wg  = None # TODO sync.WaitGroup
        self.finished = False
        self.events = []


    def Initialize(self):
        self.wg.Add(1)    


    def Add(self, event):
        self.lock.Lock()
        # TODO defer self.lock.Unlock()

        self.events = append(self.events, event)
        self.cond.Signal()


    def Stop(self):
        self.lock.Lock()

        if not self.finished:
            # TODO defer self.wg.Wait()
            pass
        
        # TODO defer self.lock.Unlock()

        self.finished = true
        self.cond.Broadcast()


    def Dispatch(self):
        self.lock.Lock()
        # TODO defer self.lock.Unlock()
        # TODO defer self.wg.Done()

        while not self.finished:
            if len(self.events) == 0:
                self.cond.Wait()
            else:
                event = self.events[0]
                self.events = self.events[1:]

                self.lock.Unlock()
                event()
                self.lock.Lock()                

