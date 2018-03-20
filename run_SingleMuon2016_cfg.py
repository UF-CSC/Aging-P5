# UF Framework specifics
from Core.Sequence import Sequence
from Core.OutputInfo import OutputInfo 

from Dataset.SingleMuon2016 import *

from Analyzer.GasGainAnalyzer import GasGainPlotter

componentList       = comp_SingleMuon2016F_v1_anl
nCores              = 1
disableProgressBar  = False
nEvents             = 100000
outputDir           = "/raid/raid7/lucien/CSC/GasGain/Log/2018-03-19/SingleMuon2016F_v1_anl/"

sequence = Sequence()
gasGainPlotter = GasGainPlotter("GasGainPlotter")
sequence.add(gasGainPlotter)

outputInfo = OutputInfo("OutputInfo")
outputInfo.outputDir = outputDir
outputInfo.TFileName = "test1.root"
