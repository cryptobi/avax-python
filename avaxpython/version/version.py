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


from avaxpython.errors import errors


defaultAppSeparator     = "/"
defaultVersionSeparator = "."
errDifferentApps  = Exception("different applications")
errDifferentMajor = Exception("different major version")


class version:

    def __init__(self, app, major, minor, patch, tostr):
        self.app = app
        self.major = major
        self.minor = minor
        self.patch = patch
        self.tostr = tostr


    def App(self):
        return self.app


    def Major(self):
        return self.major


    def Minor(self):
        return self.minor


    def Patch(self):
        return self.patch


    def String(self):
        return self.tostr


    def Compatible(self, o):
        
        if self.App() != o.App():
            return errDifferentApps

        if self.Major() > o.Major():
            return errDifferentMajor

        return None


    def Before(self, o):

        if self.App() != o.App():
            return False        

        v = self.Major()
        o = o.Major()
        
        if v < o:
            return True

        if v > o:
            return False

        v = v.Minor()
        o = o.Minor()
        
        if v < o:
            return True
        
        if v > o:
            return False

        v = v.Patch()
        o = o.Patch()

        if v < o:
            return True

        return False


# NewDefaultVersion returns a new version with default separators
def NewDefaultVersion(app, major, minor, patch):
	return NewVersion(app, defaultAppSeparator, defaultVersionSeparator, major, minor, patch)


# NewVersion returns a new version
def NewVersion(app, appSeparator, versionSeparator, major, minor, patch):
    v_string = "%s%s%d%s%d%s%d", (app, appSeparator, major, versionSeparator, minor, versionSeparator, patch)
    return version(app=app, major=major, minor=minor, patch=patch, tostr=v_string)


class parser:

    def __init__(self, sep, vsep):
        self.appSeparator = sep
        self.versionSeparator = vsep

    def Parse(self, s):

        splitApp = s.split(p.appSeparator)
        if len(splitApp) != 2:
            return nil, fmt.Errorf("failed to parse %s as a version", s)
        
        splitVersion = strings.SplitN(splitApp[1], p.versionSeparator, 3)
        if len(splitVersion) != 3:
            return nil, fmt.Errorf("failed to parse %s as a version", s)
        
        major, err = strconv.Atoi(splitVersion[0])
        if err != nil:
            return nil, fmt.Errorf("failed to parse %s as a version due to %w", s, err)
    

        minor, err = strconv.Atoi(splitVersion[1])
        if err != nil:
            return nil, fmt.Errorf("failed to parse %s as a version due to %w", s, err)
        

        patch, err = strconv.Atoi(splitVersion[2])
        if err != nil:
            return nil, fmt.Errorf("failed to parse %s as a version due to %w", s, err)       

        return NewVersion(splitApp[0], p.appSeparator, p.versionSeparator, major, minor, patch,), None



def NewDefaultParser(): 
    return NewParser(defaultAppSeparator, defaultVersionSeparator)


def NewParser(appSeparator, versionSeparator):
	return parser(appSeparator, versionSeparator)
    

