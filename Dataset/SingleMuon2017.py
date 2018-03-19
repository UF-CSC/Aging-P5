from Dataset.Utils import makeComponentsFromPath

paths_SingleMuon2017E_v1_partial = ["/cms/data/store/user/klo/CSC/CSCNTuple/SingleMuonRun2017E-v1/SingleMuon/Run2017E-PromptReco-v1/180315_115213/000%s"%i for i in range(0,7) ]

comp_SingleMuon2017E_v1_partial = []
for path in paths_SingleMuon2017E_v1_partial:
    comp_SingleMuon2017E_v1_partial.extend(makeComponentsFromPath(path))


