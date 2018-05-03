# UF Framework specifics
from Core.Sequence import Sequence
from Core.EndSequence import EndSequence
from Core.OutputInfo import OutputInfo 

from Dataset.Utils import makeComponentsFromPath
from Core.Component import Component

from Skimmer.ZMuMuSkimmer import SkimTreeZMuMuSkimmer
from Analyzer.GasGainAnalyzer import SkimTreeGasGainPlotter,SkimTreePositionPlotter
from Analyzer.RunAnalyzer import SkimTreeRunPlotter
from EndModule.GasGainEndModule import SkimTreeGasGainEndModule 

paths_SingleMuon2017E_v1_skim = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/SingleMuon2017E_v1_partial_hadd/"]
paths_SingleMuon2017E_v2_skim = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-04-08/SingleMuon2017E_v2_partial_hadd/"]
paths_SingleMuon2017E_v3_skim = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-04-15/SingleMuon2017E_v3_partial_hadd/"]
paths_SingleMuon2017E_v4_skim = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-04-15/SingleMuon2017E_v4_partial_hadd/"]

x_segments = [-150+i*15 for i in range(0,21)]
y_segments = [-200+i*20 for i in range(0,21)]

paths = paths_SingleMuon2017E_v4_skim
componentList = []
for path in paths:
    tmp = Component(path+"/",path.split("/")[-1],keyword="ME11",inUFTier2=False)
    componentList.extend(tmp.makeComponentFromEachFile())

rootTree            = "tree"
nCores              = 10 
disableProgressBar  = False
nEvents             = -1
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all_ZMuMu/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all_ZMuMu_allChannel/"

#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-04-08/comp_SingleMuon2017E_v2_skim_anl_all_ZMuMu_allChannel/"
outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-05-03/comp_SingleMuon2017E_v3_skim_anl_all_ZMuMu_allChannel_CombinedME11ab/"
justEndSequence     = True 

sequence = Sequence()
sequence.add(SkimTreeZMuMuSkimmer("ZMuMuSkimmer"))
gasGainPlotter = SkimTreeGasGainPlotter("GasGainPlotter",x_segments,y_segments)
posPlotter = SkimTreePositionPlotter("SkimTreePositionPlotter",x_segments,y_segments)
skimTreeRunPlotter = SkimTreeRunPlotter("RunPlotter")
sequence.add(gasGainPlotter)
sequence.add(posPlotter)
sequence.add(skimTreeRunPlotter)

endSequence = EndSequence()
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-03-21/InclusiveSelection/"
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-03-21/ZMuMuSelection/"
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-04-16/ZMuMuSelection_ExcludeBadChannels/"
endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-05-03/ZMuMuSelection_ExcludeBadChannels_PosStep20_CombinedME11ab/"
skimTreeGasGainEndModule = SkimTreeGasGainEndModule(endModuleOutputDir)
endSequence.add(skimTreeGasGainEndModule)

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
