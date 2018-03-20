# UF Framework specifics
from Core.Sequence import Sequence
from Core.OutputInfo import OutputInfo 

from Dataset.SingleMuon2017 import *

from Analyzer.GasGainAnalyzer import GasGainPlotter

componentList       = comp_SingleMuon2017E_v1_partial_anl_split
nCores              = 5
disableProgressBar  = False
nEvents             = -1
outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/SingleMuon2017E_v1_partial_anl/"

sequence = Sequence()
gasGainPlotter = GasGainPlotter("GasGainPlotter")
sequence.add(gasGainPlotter)

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
