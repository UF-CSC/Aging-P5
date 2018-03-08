from Core.CSCNTupleResult.Component import Component
from Core.Utils.UFTier2Utils import listdir_uberftp

import os

def makeComponentsFromPath(path):
    return [Component(n.replace(".root","").split("_")[-1]+"_",os.path.join(path,n)) for n in listdir_uberftp(path) if n.endswith(".root")]

paths_SingleMuon2016H_v2 = ["/cms/data/store/user/hmei/rootfiles_2017/CSCNtuples_2016SingleMu_BCDEFGH_promptReco/SingleMuon/crab_SingleMuon_Run2016H-PromptReco-v2/170522_130029/000%s/"%i for i in range(0,7) ]

path_SingleMuon2016H_v3 = "/cms/data/store/user/hmei/rootfiles_2017/CSCNtuples_2016SingleMu_BCDEFGH_promptReco/SingleMuon/crab_SingleMuon_Run2016H-PromptReco-v3/170322_174443/0000/"

comp_SingleMuon2016H_v2 = []
for path in paths_SingleMuon2016H_v2:
    comp_SingleMuon2016H_v2.extend(makeComponentsFromPath(path))

comp_SingleMuon2016H_v3 = makeComponentsFromPath(path_SingleMuon2016H_v3)
