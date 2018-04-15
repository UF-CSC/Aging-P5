from Core.EndModule import EndModule

import os,ROOT,math,pickle

ROOT.gROOT.SetBatch(ROOT.kTRUE)

class SkimTreeGasGainEndModule(EndModule):
    def __init__(self,outputDir):
        self.outputDir = outputDir
        self.trimRatio = 0.7
        self.makeBadChannelList()

    def makeBadChannelList(self):
        disHVFilePath = os.environ['BASE_PATH']+"/Data/BadHVChannel/hv_disabled_channels.pkl"
        self.disHVList = pickle.load(open(disHVFilePath,"r"))
        weakHVFilePath = os.environ['BASE_PATH']+"/Data/BadHVChannel/hv_weak_channels.pkl"
        self.weakHVList = pickle.load(open(weakHVFilePath,"r"))

    @staticmethod
    def convert_rhid(rhidStr):
        endcap_unit = 1000000
        station_unit = 100000
        ring_unit = 10000
        chamber_unit = 100
        layer_unit = 10
        hvseg_unit = 1
        rhid = int(rhidStr)
        endcap  = rhid // endcap_unit
        station = (rhid - endcap*endcap_unit) // station_unit 
        ring    = (rhid - endcap*endcap_unit - station*station_unit) // ring_unit 
        chamber = (rhid - endcap*endcap_unit - station*station_unit - ring*ring_unit) // chamber_unit
        layer   = (rhid - endcap*endcap_unit - station*station_unit - ring*ring_unit - chamber*chamber_unit) // layer_unit
        hvseg   = (rhid - endcap*endcap_unit - station*station_unit - ring*ring_unit - chamber*chamber_unit - layer*layer_unit) // hvseg_unit

        return [endcap,station,ring,chamber,layer,hvseg] 

    @staticmethod
    def convert_key(inputList):
        [endcap,station,ring,chamber,layer,hvseg] = inputList
        if endcap == 1:
            endcapStr = "+"
        elif endcap == 2:
            endcapStr = "-"
        prefixStr = "ME"+endcapStr+str(station)
        chamberStr = str(chamber) if chamber > 9 else "0"+str(chamber)
        if station == 1 and (ring == 1 or ring == 4):
            keyStr = "/".join([prefixStr,str(ring),chamberStr,str(layer)])
        else:
            keyStr = "/".join([prefixStr,str(ring),chamberStr,str(layer),"HVSegment"+str(hvseg)])
        return keyStr
    
    def make1DSummaryHist(self,collector,outputDir):
        c = ROOT.TCanvas()

        textFile            = open(outputDir+"Outlier.txt","w")
        badChTextFile       = open(outputDir+"BadChannel.txt","w")
        outputFile          = ROOT.TFile(outputDir+"GasGain_1DSummaryHist.root","RECREATE")
        h_trim_summary      = ROOT.TH1D("h_trim_summary","Gas Gain Summary (Trim Mean)",len(collector.samples),-0.5,len(collector.samples)-0.5)
        h_trim_1D           = ROOT.TH1D("h_trim_1D","Gas Gain 1D (Trim Mean)",1500,0,1500)
        h_trim_1D_ME11      = ROOT.TH1D("h_trim_1D_ME11","Gas Gain 1D, ME11 (Trim Mean)",1500,0,1500)
        h_trim_1D_MEX1      = ROOT.TH1D("h_trim_1D_MEX1","Gas Gain 1D, MEX1 (Trim Mean)",1500,0,1500)
        h_trim_1D_non_MEX1  = ROOT.TH1D("h_trim_1D_non_MEX1","Gas Gain 1D, ME11 (Trim Mean)",1500,0,1500)
        h_trim_corrected_1D = ROOT.TH1D("h_trim_corrected_1D","Gas Gain 1D (Trim Mean Corrected)",1500,0,5)
        h_entry_1D          = ROOT.TH1D("h_entry_1D","Number of entries 1D",100,0,10000)
        for isample,sample in enumerate(collector.samples):
            hist = collector.getObj(sample,""+sample)
            trimHist = self.makeTrimHist(hist)
            h_trim_summary.SetBinContent(isample+1,trimHist.GetMean())
            h_trim_summary.SetBinError(isample+1,trimHist.GetRMS()/math.sqrt(trimHist.Integral()))
            h_trim_summary.GetXaxis().SetBinLabel(isample+1,sample)
            for key in collector.fileDict[sample].GetListOfKeys():
                if key.GetName().startswith("ME"): continue
                rhidList = self.convert_rhid(key.GetName().replace("SumQ",""))
                detidStr =  self.convert_key(rhidList)
                if detidStr in self.disHVList or detidStr in self.weakHVList: 
                    print "Skipping", detidStr
                    continue
                hist = collector.getObj(sample,key.GetName())
                trimHist1D = self.makeTrimHist(hist) 
                h_trim_1D.Fill(trimHist1D.GetMean())
                h_trim_corrected_1D.Fill(trimHist1D.GetMean()/trimHist.GetMean())
                h_entry_1D.Fill(hist.GetEntries())
                if hist.GetEntries() < 10:
                    badChTextFile.write(" ".join([detidStr,key.GetName(),sample,])+"\n")
                if abs(trimHist1D.GetMean()/trimHist.GetMean()) < 0.84 or abs(trimHist1D.GetMean()/trimHist.GetMean()) > 1.16: 
                    textFile.write(" ".join([detidStr,key.GetName(),sample,"%4.2f"%abs(trimHist1D.GetMean()/trimHist.GetMean())])+"\n")
                if sample[2:4] == "11": # ME11
                    h_trim_1D_ME11.Fill(trimHist1D.GetMean())
                elif sample[3:4] == "1": #MEX1
                    h_trim_1D_MEX1.Fill(trimHist1D.GetMean())
                else:
                    h_trim_1D_non_MEX1.Fill(trimHist1D.GetMean()) 

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
        outputFile.Close()

        textFile.close()


    def makeAvgGasGain(self,collector):
        histDict = {}
        for isample,sample in enumerate(collector.samples):
            hist = collector.getObj(sample,""+sample)
            if sample[2:4] == "11": # ME11
                histKey = "ME11"
            elif sample[3:4] == "1": #MEX1
                histKey = "MEX1"
            else:
                histKey = "MEX234"
            if histKey not in histDict:
                histDict[histKey] = hist
            else:
                histDict[histKey].Add(hist)
        
        for histKey,sumHist in histDict.iteritems():
            trimSumHist = self.makeTrimHist(sumHist)
            print "Trimmed mean with "+histKey+": "+str(trimSumHist.GetMean())

    def makeEntriesHist(self,collector,outputDir):
        outDir = outputDir+"/Entries/"
        if not os.path.exists(os.path.abspath(outDir)):
            os.makedirs(os.path.abspath(outDir))
        
        histDict = {}
        c = ROOT.TCanvas()
        for isample,sample in enumerate(collector.samples):
            histDict[sample] = ROOT.TH1D("h_entry_1D_"+sample,"Number of entries 1D "+sample,100,0,10000)
            for key in collector.fileDict[sample].GetListOfKeys():
                if key.GetName().startswith("ME"): continue
                rhidList = self.convert_rhid(key.GetName().replace("SumQ",""))
                detidStr =  self.convert_key(rhidList)
                if detidStr in self.disHVList or detidStr in self.weakHVList: continue
                hist = collector.getObj(sample,key.GetName())
                histDict[sample].Fill(hist.GetEntries())
            histDict[sample].Draw()
            c.SaveAs(outDir+"/"+sample+".png")
        self.EntriesHistDict = histDict

    def __call__(self,collector):

        outputDir = self.outputDir
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))

        collector.samples.sort()
        self.makeEntriesHist(collector,outputDir)
        self.make1DSummaryHist(collector,outputDir)
        self.makeAvgGasGain(collector)

        c = ROOT.TCanvas()
        for isample,sample in enumerate(collector.samples):
            hist = collector.getObj(sample,""+sample)
            hist.SetStats(0)
            hist.Draw()
            c.SaveAs(outputDir+sample+".png")


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
        

