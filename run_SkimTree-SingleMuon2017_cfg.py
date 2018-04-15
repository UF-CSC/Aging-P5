# UF Framework specifics
from Core.Sequence import Sequence
from Core.EndSequence import EndSequence
from Core.OutputInfo import OutputInfo 

from Dataset.Utils import makeComponentsFromPath
from Core.NanoAODResult.Component import Component

from Skimmer.ZMuMuSkimmer import SkimTreeZMuMuSkimmer
from Analyzer.GasGainAnalyzer import SkimTreeGasGainPlotter
from Analyzer.RunAnalyzer import SkimTreeRunPlotter
from EndModule.GasGainEndModule import SkimTreeGasGainEndModule 

paths_SingleMuon2017E_v1_skim = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/SingleMuon2017E_v1_partial_hadd/"]
paths_SingleMuon2017E_v2_skim = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-04-08/SingleMuon2017E_v2_partial_hadd/"]

paths = paths_SingleMuon2017E_v2_skim
componentList = []
for path in paths:
    tmp = Component(path+"/",path.split("/")[-1],keyword="",inUFTier2=False)
    componentList.extend(tmp.makeComponentFromEachFile())

rootTree            = "tree"
nCores              = 8
disableProgressBar  = False
nEvents             = -1
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all_ZMuMu/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all_ZMuMu_allChannel/"
outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-04-08/comp_SingleMuon2017E_v2_skim_anl_all_ZMuMu_allChannel/"
justEndSequence     = True 

sequence = Sequence()
sequence.add(SkimTreeZMuMuSkimmer("ZMuMuSkimmer"))
gasGainPlotter = SkimTreeGasGainPlotter("GasGainPlotter")
skimTreeRunPlotter = SkimTreeRunPlotter("RunPlotter")
sequence.add(gasGainPlotter)
sequence.add(skimTreeRunPlotter)

endSequence = EndSequence()
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-03-21/InclusiveSelection/"
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-03-21/ZMuMuSelection/"
endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-04-09/ZMuMuSelection_ExcludeBadChannels/"
skimTreeGasGainEndModule = SkimTreeGasGainEndModule(endModuleOutputDir)
endSequence.add(skimTreeGasGainEndModule)

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
