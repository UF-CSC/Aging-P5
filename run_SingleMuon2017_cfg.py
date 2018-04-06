# UF Framework specifics
from Core.Sequence import Sequence
from Core.EndSequence import EndSequence
from Core.OutputInfo import OutputInfo 

from Dataset.SingleMuon2017 import *

from Analyzer.GasGainAnalyzer import GasGainPlotter
from Analyzer.RunAnalyzer import RunPlotter

componentList       = comp_SingleMuon2017E_v1_partial_anl_split[0:1]
nCores              = 5
disableProgressBar  = False
nEvents             = -1
outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-04-05/SingleMuon2017E_v1_partial_anl/"

sequence = Sequence()
gasGainPlotter  = GasGainPlotter("GasGainPlotter")
runPlotter      = RunPlotter("RunPlotter")
#sequence.add(gasGainPlotter)
sequence.add(runPlotter)

endSequence = EndSequence()

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
