# avax-python : Python tools for the exploration of the Avalanche AVAX network.
# Author: https://github.com/ojrdevcom/
# License MIT

# Translate api.spec to avapython
# See tatsu grammar syntax https://tatsu.readthedocs.io/en/stable/syntax.html

import re
import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
import json

GRAMMAR_FILE = "api.tatsu"
SPEC_FILE = "api.specification"


class AvaField():
    """
        Convenience class to encapsulate an API field (parameter or return).
        If avatype is a recursive type, it'll contain an array / subset of return types.
    """
    def __init__(self, name, avatype, optional):
        self.name = name
        self.avatype = avatype
        self.optional = optional

    def __repr__(self):
        mystr = "AvaField( " + str(self.name) + ": " + str(self.avatype)
        if (self.optional):
            mystr += " (Optional) "
        
        mystr += " ) "
        
        return mystr


class AvaMethod():
    """Convenience class to encapsulate an API method."""
    def __init__(self, package, methodx, params, returns):
        self.package = package
        self.methodx = methodx
        self.params = params
        self.returns = returns

    def __repr__(self):
        return "AvaMethod( " + self.package + "." + self.methodx + "(" + str(self.params) + ") -> " + str(self.returns) + " )"


class AvaEndpoint():
    """Convenience class to encapsulate an API endpoint and its methods."""
    def __init__(self, endpoint, methods):
        self.endpoint = endpoint
        self.methods = methods

    def __repr__(self):
        return "AvaEndpoint( " + self.endpoint + " -> " + str(self.methods) + " )"


class AvaApi():
    """Convenience class to encapsulate an AVA API."""
    def __init__(self, endpoints):
        self.endpoints = endpoints

    def __repr__(self):
        return "AvaApi( " + str(self.endpoints) + " )"


def read_spec(specfil):
    """Reads de API spec file into endpoint-delimited sections"""

    rk = {}
    curr_ep = "error"  # invalid endpoint [indicates a parsing problem]
    rgx = re.compile("^endpoint:\\s*([^\\s]+)")

    with open(specfil, "r") as f:
        
        lin = f.readline()
        grp = ""

        while lin:
            
            m = rgx.search(lin.strip())

            if m:             
                curr_ep = m[1]
            elif lin.strip() == "":
                if curr_ep in rk:
                    rk[curr_ep].append(grp)
                else:
                    rk[curr_ep] = [grp]
            
                grp = ""
            else:
                grp += lin  

            lin = f.readline()

    return rk            


def walk_fields(part):
    """
        part is an array of fields from the AST.
        Types are represented by arrays of format [name,semicolon,type[,comma_or_array[,maybe_comma]]]
        The field tree is built recursively.
        For part lengths 3 and 4 we shortcircuit the special cases. 
        All others are senth through recursion.
    """
    ret = []                                                

    for mx in part:
        
        lx = len(mx)

        if isinstance(mx, list):
            # fields always have 2nd entry == ":"
            if not (lx >= 3 and mx[1] == ":"):                
                return walk_fields(mx)
        
        if mx == "{" or mx == "}":
            continue

        if lx == 3:                                
            # scalar type
            fld = AvaField(mx[0], mx[2], False)
            ret.append(fld); 
            continue

        if lx > 3:

            if mx[3] == "(optional)":
                fld = AvaField(mx[0], mx[2], True)
                continue

            if lx == 4:             

                if mx[3] == ",":
                    fld = AvaField(mx[0], mx[2], False)
                    ret.append(fld); 
                    continue            
                
                if mx[2] == "[]":
                    fld = AvaField(mx[0], None, False)
                    fld.avatype = AvaField("[]", mx[3], False)
                    ret.append(fld); 
                    continue

            if lx > 4:
                
                fld = AvaField(mx[0], mx[2], False)

                if mx[4] == "(optional)":         
                    fld.optional = True           
                    continue                

                if mx[2] == "{":                
                    fld.avatype = AvaField("{}", walk_fields(mx[3]), False)
                    ret.append(fld); 
                    continue 

                if mx[2] == "[]":                
                    fld.avatype = AvaField("[]", walk_fields(mx[4]), False)
                    ret.append(fld); 
                    continue 

                print("SYNTAX ERROR. CHECK GRAMMAR FOR UNTREATED CASES.\nLENGTH {} \nMX {} \nPART {}".format(lx, mx, part))
                exit(1)  

    return ret


def parse_api(spec_file, grammar_file):

    api = AvaApi([])
    apispec = read_spec(spec_file)

    grammar = open(grammar_file, 'r').read()
    parser = tatsu.compile(grammar) 

    for endpoint, v in apispec.items():
        ep = AvaEndpoint(endpoint, [])
        for chunk in v:            
            if len(chunk.strip()) > 0:    

                ix = parser.parse(chunk)   
                           
                package, methodx = ix[0].split(".")                
                mth = AvaMethod(package, methodx, [], [])

                for inx in range(2, len(ix)):
                    part = ix[inx]
                     
                    if part == "}" or part == "{":
                        continue

                    if isinstance(part, list):
                        mth.params = walk_fields(part)                        

                    if part == "->":                        
                        mth.returns = walk_fields(ix[inx+1])                                                    
                        break # end tree processing                

                                           
                ep.methods.append(mth)                    

        api.endpoints.append(ep)

    return api        


def render_txt(api):
    for endpoint in api.endpoints:
        print(endpoint.endpoint)
        for mtx in endpoint.methods:
            print("\t{}".format(mtx))


def render_list_field(flds):

    out_struct = []

    for prm in flds:   

        if isinstance(prm.avatype, AvaField):
            out_struct.append({
                "type": render_dict_field([prm.avatype]),
                "optional": prm.optional
            })
        elif isinstance(prm.avatype, list):
            newtype = render_list_field(prm.avatype)
            out_struct.append({
                "type": newtype,
                "optional": prm.optional
            })
        else:
            out_struct.append({
                "type": prm.avatype,
                "optional": prm.optional
            })       

    return out_struct


def render_dict_field(flds):

    out_struct = {}

    for prm in flds:   

        if prm.name not in out_struct:
            out_struct[prm.name] = {}

        if isinstance(prm.avatype, AvaField):
            out_struct[prm.name] = {
                "type": render_dict_field([prm.avatype]),
                "optional": prm.optional
            }
        elif isinstance(prm.avatype, list):
            newtype = []
        else:
            out_struct[prm.name] = {
                "type": prm.avatype,
                "optional": prm.optional
            }                        

    return out_struct


def render_dict(api):

    out_struct = {}

    for endpoint in api.endpoints:

        ep = endpoint.endpoint
        out_struct[ep] = {}

        for mtx in endpoint.methods:
            if mtx.package not in out_struct[ep]:
                out_struct[ep][mtx.package] = {}

            if mtx.methodx not in out_struct[ep][mtx.package]:
                out_struct[ep][mtx.package][mtx.methodx] = {}
                out_struct[ep][mtx.package][mtx.methodx]["parameters"] = render_dict_field(mtx.params)
                out_struct[ep][mtx.package][mtx.methodx]["returns"] = render_dict_field(mtx.returns)

    return out_struct                


def render_json(api):    
    return json.dumps(render_dict(api), sort_keys=True, indent=4)


if __name__ == "__main__":
    
    api = parse_api(SPEC_FILE, GRAMMAR_FILE)
    outx = render_json(api)
    print(outx)
            