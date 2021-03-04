# UF Framework specifics
from Core.Sequence import Sequence
from Core.EndSequence import EndSequence
from Core.OutputInfo import OutputInfo
from Core.ComponentList import *

from Core.Dataset import Dataset

from Skimmer.ZMuMuSkimmer import SkimTreeZMuMuSkimmer
from Analyzer.GasGainAnalyzer import SkimTreeGasGainPlotter,SkimTreePositionPlotter
from Analyzer.RunAnalyzer import SkimTreeRunPlotter
from EndModule.GasGainEndModule import SkimTreeGasGainEndModule,SkimTreePositionEndModule 

from Config.Chamber import *

import os

inputDir = "/cmsuf/data/store/user/t2/users/klo/CSC/Skim/210304_Data_2017A_hadd/"
componentList = []
for f in os.listdir(inputDir):
    fname = f.replace(".root","")
    tmp = Dataset(
        "SingleMuon_2017A_Skim_"+fname,
        ComponentList([
            Component(
                fname,
                os.path.join(inputDir,f),
                "tree",False)
        ]),
        )
    componentList.append(tmp)

rootTree            = "tree"
nCores              = 10 
disableProgressBar  = False
nEvents             = -1
outputDir           = "output/GasGain_2021-03-04/"
justEndSequence     = True 

sequence = Sequence()
sequence.add(SkimTreeZMuMuSkimmer("ZMuMuSkimmer"))
gasGainPlotter = SkimTreeGasGainPlotter("GasGainPlotter")
posPlotter = SkimTreePositionPlotter("SkimTreePositionPlotter",y_segment_dict)
skimTreeRunPlotter = SkimTreeRunPlotter("RunPlotter")
sequence.add(gasGainPlotter)
sequence.add(skimTreeRunPlotter)

endSequence = EndSequence(skipHadd=justEndSequence)
endModuleOutputDir = outputDir
skimTreeGasGainEndModule = SkimTreeGasGainEndModule(endModuleOutputDir)
endSequence.add(skimTreeGasGainEndModule)
skimTreePositionEndModule = SkimTreePositionEndModule(endModuleOutputDir,ChamberTypes,y_segment_dict,normalize=True)
endSequence.add(skimTreePositionEndModule)

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
