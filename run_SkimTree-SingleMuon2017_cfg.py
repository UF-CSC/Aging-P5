# UF Framework specifics
from Core.Sequence import Sequence
from Core.EndSequence import EndSequence
from Core.OutputInfo import OutputInfo 

from Dataset.Utils import makeComponentsFromPath
from Core.Component import Component

from Skimmer.ZMuMuSkimmer import SkimTreeZMuMuSkimmer
from Analyzer.GasGainAnalyzer import SkimTreeGasGainPlotter,SkimTreePositionPlotter
from Analyzer.RunAnalyzer import SkimTreeRunPlotter
from EndModule.GasGainEndModule import SkimTreeGasGainEndModule,SkimTreePositionEndModule 

from Config.Chamber import *

pathStr = "paths_SingleMuon2017H_ZMu_v1_skim"
compStr = pathStr.replace("paths","comp")

paths_SingleMuon2017A_ZMu_v2_skim   = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017A_ZMu_v2_partial_hadd/"]
paths_SingleMuon2017B_ZMu_v1_skim   = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017B_ZMu_v1_partial_hadd/"]
paths_SingleMuon2017C_ZMu_v1_skim   = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017C_ZMu_v1_partial_hadd/"]
paths_SingleMuon2017D_v1_skim       = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017D_v1_partial_hadd/"]
paths_SingleMuon2017E_v2_skim       = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017E_v2_partial_hadd/"]
paths_SingleMuon2017F_ZMu_v1_skim   = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017F_ZMu_v1_partial_hadd/"]
paths_SingleMuon2017G_ZMu_v1_skim   = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017G_ZMu_v1_partial_hadd/"]
paths_SingleMuon2017H_ZMu_v1_skim   = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-05-06/comp_SingleMuon2017H_ZMu_v1_partial_hadd/"]
#paths_SingleMuon2017E_v1_skim       = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/SingleMuon2017E_v1_partial_hadd/"]
#paths_SingleMuon2017E_v2_skim       = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-04-08/SingleMuon2017E_v2_partial_hadd/"]
#paths_SingleMuon2017E_v3_skim       = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-04-15/SingleMuon2017E_v3_partial_hadd/"]
#paths_SingleMuon2017E_v4_skim       = ["/raid/raid7/lucien/CSC/GasGain/Log/2018-04-15/SingleMuon2017E_v4_partial_hadd/"]

paths = eval(pathStr)
componentList = []
for path in paths:
    tmp = Component(path+"/",path.split("/")[-1],inUFTier2=False)
    componentList.extend(tmp.makeComponentFromEachFile())

rootTree            = "tree"
nCores              = 10 
disableProgressBar  = False
nEvents             = -1
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all_ZMuMu/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/comp_SingleMuon2017E_v1_skim_anl_all_ZMuMu_allChannel/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-04-08/comp_SingleMuon2017E_v2_skim_anl_all_ZMuMu_allChannel/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-05-03/comp_SingleMuon2017E_v3_skim_anl_all_ZMuMu_allChannel_CombinedME11ab/"
#outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-05-03/comp_SingleMuon2017E_v3_skim_anl_all_ZMuMu_allChannel_CombinedME11ab_yloc/"
outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-05-07/"+compStr+"_anl/"
justEndSequence     = False 

sequence = Sequence()
sequence.add(SkimTreeZMuMuSkimmer("ZMuMuSkimmer"))
gasGainPlotter = SkimTreeGasGainPlotter("GasGainPlotter")
posPlotter = SkimTreePositionPlotter("SkimTreePositionPlotter",y_segment_dict)
skimTreeRunPlotter = SkimTreeRunPlotter("RunPlotter")
sequence.add(gasGainPlotter)
sequence.add(posPlotter)
sequence.add(skimTreeRunPlotter)

endSequence = EndSequence()
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-03-21/InclusiveSelection/"
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-03-21/ZMuMuSelection/"
#endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-04-16/ZMuMuSelection_ExcludeBadChannels/"
endModuleOutputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-05-07/"+compStr+"_anl/"
skimTreeGasGainEndModule = SkimTreeGasGainEndModule(endModuleOutputDir)
endSequence.add(skimTreeGasGainEndModule)
skimTreePositionEndModule = SkimTreePositionEndModule(endModuleOutputDir,ChamberTypes,y_segment_dict,normalize=True)
endSequence.add(skimTreePositionEndModule)

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
