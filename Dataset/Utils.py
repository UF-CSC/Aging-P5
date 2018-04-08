from Core.CSCNTupleResult.Component import Component
from Core.Utils.UFTier2Utils import listdir_uberftp

import os

def makeComponentsFromPath(path,prefix=""):
    return [Component(prefix+n.replace(".root","").split("_")[-1]+"_",os.path.join(path,n)) for n in listdir_uberftp(path) if n.endswith(".root")]
