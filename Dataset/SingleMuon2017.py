from Dataset.Utils import makeComponentsFromPath
from Core.NanoAODResult.Component import Component

paths_SingleMuon2017E_v1_partial = ["/cms/data/store/user/klo/CSC/CSCNTuple/SingleMuonRun2017E-v1/SingleMuon/Run2017E-PromptReco-v1/180315_115213/000%s"%i for i in range(0,7) ]

comp_SingleMuon2017E_v1_partial = []
for path in paths_SingleMuon2017E_v1_partial:
    comp_SingleMuon2017E_v1_partial.extend(makeComponentsFromPath(path,path.split("/")[-1]))

comp_SingleMuon2017E_v1_partial_anl = []
comp_SingleMuon2017E_v1_partial_anl_split = []
for path in paths_SingleMuon2017E_v1_partial:
    tmp = Component(path+"/",path.split("/")[-1],keyword="")
    comp_SingleMuon2017E_v1_partial_anl.append(tmp)
    comp_SingleMuon2017E_v1_partial_anl_split.extend(tmp.makeComponentFromEachFile(prefix=path.split("/")[-1]+"-"))
