from CSCNTupleResult.Component import Component

import os

def makeComponentsFromPath(path,prefix=""):
    return [Component(prefix+n.replace(".root","").split("_")[-1]+"_",os.path.join(path,n)) for n in os.listdir(path) if n.endswith(".root")]
