from Core.EndModule import EndModule

import os,ROOT,math

ROOT.gROOT.SetBatch(ROOT.kTRUE)

class SkimTreeGasGainEndModule(EndModule):
    def __init__(self,outputDir):
        self.outputDir = outputDir
        self.trimRatio = 0.7

    def __call__(self,collector):
        c = ROOT.TCanvas()
        outputDir = self.outputDir
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))
        outputFile = ROOT.TFile(outputDir+"SkimTreeGasGain.root","RECREATE")
        h_trim_summary = ROOT.TH1D("h_trim_summary","Gas Gain Summary (Trim Mean)",len(collector.samples),-0.5,len(collector.samples)-0.5)
        collector.samples.sort()
        for isample,sample in enumerate(collector.samples):
            hist = collector.getObj(sample,""+sample)
            hist.SetStats(0)
            hist.Draw()
            c.SaveAs(outputDir+sample+".png")
            trimHist = self.makeTrimHist(hist)
            h_trim_summary.SetBinContent(isample+1,trimHist.GetMean())
            h_trim_summary.SetBinError(isample+1,trimHist.GetRMS()/math.sqrt(trimHist.Integral()))
            h_trim_summary.GetXaxis().SetBinLabel(isample+1,sample)
        h_trim_summary.SetStats(0)
        h_trim_summary.GetXaxis().SetLabelSize(0.025)
        h_trim_summary.Draw()
        c.SaveAs(outputDir+"trim_mean_summary.png")
        outputFile.Write()

    def makeTrimHist(self,hist):
        trimHist = hist.Clone(hist.GetName()+"_trim")
        integral = 0.
        normalisation = hist.Integral()
        for ibin in range(1,trimHist.GetNbinsX()+1):
            if integral < self.trimRatio*normalisation:
                integral += hist.GetBinContent(ibin)
            else:
                trimHist.SetBinContent(ibin,0)
        return trimHist
        

