from Dataset.Utils import makeComponentsFromPath
from Core.Component import Component

def makeComponentList(pathTemplate,no_of_dir,prefix="SingleMuon"):
    paths = [pathTemplate+str(i)+"/" for i in range(0,no_of_dir+1)]
    comps = []
    for path in paths:
        comps.extend(makeComponentsFromPath(path,prefix+"_"+path.split("/")[-1]))
    return comps

comp_SingleMuon2017B_ZMu_v1_partial         = makeComponentList("/cms/data/store/user/klo/CSC/CSCNTuple/SingleMuonRun2017B-ZMu-v1/SingleMuon/Run2017B-PromptReco-ZMu-v1/180503_104146/000",0,"SingleMuonB_ZMu_v1")
comp_SingleMuon2017C_ZMu_v1_partial         = makeComponentList("/cms/data/store/user/klo/CSC/CSCNTuple/SingleMuonRun2017C-ZMu-v1/SingleMuon/Run2017C-PromptReco-ZMu-v1/180502_162630/000",0,"SingleMuonC_ZMu_v1")
comp_SingleMuon2017E_v1_partial             = makeComponentList("/cms/data/store/user/klo/CSC/CSCNTuple/SingleMuonRun2017E-v1/SingleMuon/Run2017E-PromptReco-v1/180315_115213/000",6,"SingleMuonE_v1")
comp_SingleMuon2017H_ZMu_v1_partial         = makeComponentList("/cms/data/store/user/klo/CSC/CSCNTuple/SingleMuonRun2017H-ZMu-v1/SingleMuon/Run2017H-PromptReco-ZMu-v1/180503_103024/000",0,"SingleMuonH_ZMu_v1")

comp_SingleMuon2017_partial = comp_SingleMuon2017C_ZMu_v1_partial + comp_SingleMuon2017H_ZMu_v1_partial

def makeSkimComponentList(pathTemplate,no_of_dir):
    comp_anl = []
    comp_anl_split = []
    paths = [pathTemplate+str(i)+"/" for i in range(0,no_of_dir+1)]
    for path in paths:
        tmp = Component(path+"/",path.split("/")[-1],keyword="")
        comp_anl.append(tmp)
        comp_anl_split.extend(tmp.makeComponentFromEachFile(prefix=path.split("/")[-1]+"-"))
    return comp_anl,comp_anl_split

comp_SingleMuon2017E_v1_partial_anl,comp_SingleMuon2017E_v1_partial_anl_split = makeSkimComponentList("/cms/data/store/user/klo/CSC/CSCNTuple/SingleMuonRun2017E-v1/SingleMuon/Run2017E-PromptReco-v1/180315_115213/000",6)
