# UF Framework specifics
from Core.Sequence import Sequence
from Core.EndSequence import EndSequence
from Core.OutputInfo import OutputInfo 

from Dataset.Utils import makeComponentsFromPath
from Core.NanoAODResult.Component import Component

from Analyzer.GasGainAnalyzer import SkimTreeGasGainPlotter
from EndModule.GasGainEndModule import SkimTreeGasGainEndModule 

paths_SingleMuon2017E_v1_skim = ["/raid/raid9/lucien/CSC/GasGain/Log/2018-03-19/SingleMuon2017E_v1_partial_hadd/"]
comp_SingleMuon2017E_v1_skim = []
for path in paths_SingleMuon2017E_v1_skim:
    tmp = Component(path+"/",path.split("/")[-1],keyword="",inUFTier2=False)
    comp_SingleMuon2017E_v1_skim.extend(tmp.makeComponentFromEachFile())

rootTree            = "tree"
componentList       = comp_SingleMuon2017E_v1_skim
nCores              = 5
disableProgressBar  = False
nEvents             = -1
outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all/"
justEndSequence     = True

sequence = Sequence()
gasGainPlotter = SkimTreeGasGainPlotter("GasGainPlotter")
sequence.add(gasGainPlotter)

endSequence = EndSequence()
endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-03-21/InclusiveSelection/"
endSequence.add(SkimTreeGasGainEndModule(endModuleOutputDir))

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
