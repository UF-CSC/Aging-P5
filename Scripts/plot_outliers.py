import ROOT,sys

textFile = open("/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-04-09/ZMuMuSelection_ExcludeBadChannels/Outlier.txt","r")
lines = textFile.readlines()

baseDir = "/raid/raid7/lucien/CSC/GasGain/Log/2018-04-08/comp_SingleMuon2017E_v2_skim_anl_all_ZMuMu_allChannel/"
outputDir = "/home/lucien/public_html/CSC/GasGainAnalysis/Log/2018-04-09/ZMuMuSelection_ExcludeBadChannels/OutlierPlot/"

ROOT.gROOT.SetBatch(ROOT.kTRUE)
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
    
