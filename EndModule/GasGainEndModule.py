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
        outputFile          = ROOT.TFile(outputDir+"SkimTreeGasGain.root","RECREATE")
        textFile            = open(outputDir+"Outlier.txt","w")
        badChTextFile       = open(outputDir+"BadChannel.txt","w")
        h_trim_summary      = ROOT.TH1D("h_trim_summary","Gas Gain Summary (Trim Mean)",len(collector.samples),-0.5,len(collector.samples)-0.5)
        h_trim_1D           = ROOT.TH1D("h_trim_1D","Gas Gain 1D (Trim Mean)",1500,0,1500)
        h_trim_1D_ME11      = ROOT.TH1D("h_trim_1D_ME11","Gas Gain 1D, ME11 (Trim Mean)",1500,0,1500)
        h_trim_1D_MEX1      = ROOT.TH1D("h_trim_1D_MEX1","Gas Gain 1D, MEX1 (Trim Mean)",1500,0,1500)
        h_trim_1D_non_MEX1  = ROOT.TH1D("h_trim_1D_non_MEX1","Gas Gain 1D, ME11 (Trim Mean)",1500,0,1500)
        h_trim_corrected_1D = ROOT.TH1D("h_trim_corrected_1D","Gas Gain 1D (Trim Mean Corrected)",1500,0,5)
        h_entry_1D          = ROOT.TH1D("h_entry_1D","Number of entries 1D",100,0,2000)
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
            for key in collector.fileDict[sample].GetListOfKeys():
                hist = collector.getObj(sample,key.GetName())
                trimHist1D = self.makeTrimHist(hist)
                h_trim_1D.Fill(trimHist1D.GetMean())
                h_trim_corrected_1D.Fill(trimHist1D.GetMean()/trimHist.GetMean())
                h_entry_1D.Fill(hist.GetEntries())
                if sample[2:4] == "11": # ME11
                    h_trim_1D_ME11.Fill(trimHist1D.GetMean())
                elif sample[3:4] == "1": #MEX1
                    h_trim_1D_MEX1.Fill(trimHist1D.GetMean())
                else:
                    h_trim_1D_non_MEX1.Fill(trimHist1D.GetMean())
                if hist.GetEntries() < 10:
                    badChTextFile.write(" ".join([key.GetName(),sample,])+"\n")
                if abs(trimHist1D.GetMean()/trimHist.GetMean()) < 0.84 or abs(trimHist1D.GetMean()/trimHist.GetMean()) > 1.16: 
                    textFile.write(" ".join([key.GetName(),sample,"%4.2f"%abs(trimHist1D.GetMean()/trimHist.GetMean())])+"\n")
        h_trim_summary.SetStats(0)
        h_trim_summary.GetXaxis().SetLabelSize(0.025)
        h_trim_summary.Draw()
        c.SaveAs(outputDir+"trim_mean_summary.png")
        h_trim_1D.SetStats(0)
        h_trim_1D.GetXaxis().SetLabelSize(0.025)
        h_trim_1D.Draw()
        c.SaveAs(outputDir+"trim_mean_1D.png")
        h_entry_1D.Draw()
        c.SaveAs(outputDir+"number_of_entries.png")
        h_trim_corrected_1D.SetStats(0)
        h_trim_corrected_1D.GetXaxis().SetLabelSize(0.025)
        h_trim_corrected_1D.Draw()
        c.SaveAs(outputDir+"trim_mean_corrected_1D.png")
        c.SetLogy()
        c.SaveAs(outputDir+"trim_mean_corrected_log_1D.png")

        outputFile.Write()
        textFile.close()

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
        

