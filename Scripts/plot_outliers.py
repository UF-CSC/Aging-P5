import ROOT,sys,os

textFile = open("/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-04-16/ZMuMuSelection_ExcludeBadChannels_PosStep20_CombinedME11ab/Outlier.txt","r")
lines = textFile.readlines()

baseDir = "/raid/raid7/lucien/CSC/GasGain/Log/2018-04-16/comp_SingleMuon2017E_v3_skim_anl_all_ZMuMu_allChannel_6/"
outputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-04-16/ZMuMuSelection_ExcludeBadChannels_PosStep20_CombinedME11ab/OutlierPlot/"

ROOT.gROOT.SetBatch(ROOT.kTRUE)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
c = ROOT.TCanvas()
for line in lines:
    items = line.split()
    stationring = items[-2]
    histName = items[1]
    inputFile = ROOT.TFile(baseDir+"/"+stationring+"/test1.root","READ")
    hist = inputFile.Get(histName)
    hist.Rebin(10)
    hist.Draw()
    c.SaveAs(outputDir+histName+".png")
    
