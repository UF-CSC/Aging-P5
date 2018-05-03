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
            keyStr = "/".join([prefixStr,"1",chamberStr,str(layer)])
        else:
            keyStr = "/".join([prefixStr,str(ring),chamberStr,str(layer),"HVSegment"+str(hvseg)])
        return keyStr
    
    def make1DSummaryHist(self,collector,outputDir):
        c = ROOT.TCanvas()

        textFile                        = open(outputDir+"Outlier.txt","w")
        outputFile                      = ROOT.TFile(outputDir+"GasGain_1DSummaryHist.root","RECREATE")
        h_trim_summary                  = ROOT.TH1D("h_trim_summary","Gas Gain Summary (Trim Mean)",len(collector.samples),-0.5,len(collector.samples)-0.5)
        h_trim_1D                       = ROOT.TH1D("h_trim_1D","Gas Gain 1D (Trim Mean)",1500,0,1500)
        h_trim_1D_ME11                  = ROOT.TH1D("h_trim_1D_ME11","Gas Gain 1D, ME11 (Trim Mean)",1500,0,1500)
        h_trim_1D_MEX1                  = ROOT.TH1D("h_trim_1D_MEX1","Gas Gain 1D, MEX1 (Trim Mean)",1500,0,1500)
        h_trim_1D_non_MEX1              = ROOT.TH1D("h_trim_1D_non_MEX1","Gas Gain 1D, Others (Trim Mean)",1500,0,1500)
        h_trim_corrected_1D             = ROOT.TH1D("h_trim_corrected_1D","Gas Gain 1D (Trim Mean Corrected)",1500,0,2)
        h_trim_corrected_1D_ME11        = ROOT.TH1D("h_trim_corrected_1D_ME11","Gas Gain 1D, ME11 (Trim Mean Corrected)",1500,0,2)
        h_trim_corrected_1D_MEX1        = ROOT.TH1D("h_trim_corrected_1D_MEX1","Gas Gain 1D, MEX1 (Trim Mean Corrected)",1500,0,2)
        h_trim_corrected_1D_non_MEX1    = ROOT.TH1D("h_trim_corrected_1D_non_MEX1","Gas Gain 1D, Others (Trim Mean Corrected)",1500,0,2)
        h_entry_1D                      = ROOT.TH1D("h_entry_1D","Number of entries 1D",100,0,10000)
        for isample,sample in enumerate(collector.samples):
            if sample == "ME11a" or sample == "ME11b": continue
            hist = collector.getObj(sample,""+sample)
            trimHist = self.makeTrimHist(hist)
            h_trim_summary.SetBinContent(isample+1,trimHist.GetMean())
            h_trim_summary.SetBinError(isample+1,trimHist.GetRMS()/math.sqrt(trimHist.Integral()))
            h_trim_summary.GetXaxis().SetBinLabel(isample+1,sample)
            if sample[2:4] == "11": # ME11
                histKey = "ME11"
            elif sample[3:4] == "1": #MEX1
                histKey = "MEX1"
            else:
                histKey = "MEX234"
            for key in collector.fileDict[sample].GetListOfKeys():
                if key.GetName().startswith("ME"): continue
                if "Loc" in key.GetName(): continue
                if "SumQX" in key.GetName() or "SumQY" in key.GetName(): continue
                rhidList = self.convert_rhid(key.GetName().replace("SumQ",""))
                detidStr =  self.convert_key(rhidList)
                if detidStr in self.disHVList or detidStr in self.weakHVList: 
                    print "Skipping", detidStr
                    continue
                hist = collector.getObj(sample,key.GetName())
                trimHist1D = self.makeTrimHist(hist) 
                h_trim_1D.Fill(trimHist1D.GetMean())
                h_trim_corrected_1D.Fill(trimHist1D.GetMean()/self.avgGasGainDict[histKey].GetMean())
                h_entry_1D.Fill(hist.GetEntries())
                if abs(trimHist1D.GetMean()/trimHist.GetMean()) < 0.84 or abs(trimHist1D.GetMean()/trimHist.GetMean()) > 1.16: 
                    textFile.write(" ".join([detidStr,key.GetName(),sample,"%4.2f"%abs(trimHist1D.GetMean()/trimHist.GetMean())])+"\n")
                if sample[2:4] == "11": # ME11
                    h_trim_corrected_1D_ME11.Fill(trimHist1D.GetMean()/self.avgGasGainDict[histKey].GetMean())
                    h_trim_1D_ME11.Fill(trimHist1D.GetMean())
                elif sample[3:4] == "1": #MEX1
                    h_trim_corrected_1D_MEX1.Fill(trimHist1D.GetMean()/self.avgGasGainDict[histKey].GetMean())
                    h_trim_1D_MEX1.Fill(trimHist1D.GetMean())
                else:
                    h_trim_corrected_1D_non_MEX1.Fill(trimHist1D.GetMean()/self.avgGasGainDict[histKey].GetMean())
                    h_trim_1D_non_MEX1.Fill(trimHist1D.GetMean()) 

        h_trim_summary.SetStats(0)
        h_trim_summary.GetXaxis().SetLabelSize(0.025)
        h_trim_summary.Draw()
        c.SaveAs(outputDir+"trim_mean_summary.pdf")
        c.SaveAs(outputDir+"trim_mean_summary.png")
        h_trim_1D.SetStats(0)
        h_trim_1D.GetXaxis().SetLabelSize(0.025)
        h_trim_1D.Draw()
        c.SaveAs(outputDir+"trim_mean_1D.pdf")
        c.SaveAs(outputDir+"trim_mean_1D.png")
        h_entry_1D.Draw()
        c.SaveAs(outputDir+"number_of_entries.png")
        c.SaveAs(outputDir+"number_of_entries.pdf")
        c.SetLogy(1)
        c.SaveAs(outputDir+"number_of_entries_log.png")
        c.SaveAs(outputDir+"number_of_entries_log.pdf")
        c.SetLogy(0)
        leg = ROOT.TLegend(0.63,0.58,0.89,0.87)
        leg.SetTextSize(0.02)
        drawList = [h_trim_1D_ME11,h_trim_1D_MEX1,h_trim_1D_non_MEX1]
        maxRange = max([hist.GetMaximum() for hist in drawList])
        for ihist,hist in enumerate(drawList):
            hist.SetStats(0)
            hist.GetYaxis().SetRangeUser(0.00,maxRange*1.2)
            leg.AddEntry(hist,hist.GetTitle())
            hist.SetTitle("")
            hist.SetLineColor(ihist+1)
            if ihist:
                hist.Draw("same")
            else:
                hist.Draw()
        leg.Draw()
        c.SaveAs(outputDir+"trim_mean_1D_separate.png")
        c.SaveAs(outputDir+"trim_mean_1D_separate.pdf")
        for ihist,hist in enumerate(drawList):
            hist.GetYaxis().SetRangeUser(0.01,maxRange*1.2)
        c.SetLogy(1)
        c.SaveAs(outputDir+"trim_mean_1D_separate_log.png")
        c.SaveAs(outputDir+"trim_mean_1D_separate_log.pdf")

        drawList = [h_trim_corrected_1D_ME11,h_trim_corrected_1D_MEX1,h_trim_corrected_1D_non_MEX1]
        for hist in drawList:
            hist.Rebin(8)
            hist.Scale(1/hist.Integral())
        maxRange = max([hist.GetMaximum() for hist in drawList])
        leg = ROOT.TLegend(0.63,0.58,0.89,0.87)
        leg.SetTextSize(0.02)
        for ihist,hist in enumerate(drawList):
            hist.SetStats(0)
            hist.GetYaxis().SetRangeUser(0.00,maxRange*1.2)
            leg.AddEntry(hist,hist.GetTitle())
            hist.SetTitle("")
            hist.SetLineColor(ihist+1)
            if ihist:
                hist.Draw("same")
            else:
                hist.Draw()
        leg.Draw()
        c.SetLogy(0)
        c.SaveAs(outputDir+"trim_mean_corrected_1D_separate.png")
        c.SaveAs(outputDir+"trim_mean_corrected_1D_separate.pdf")
        for ihist,hist in enumerate(drawList):
            hist.GetYaxis().SetRangeUser(0.01,maxRange*1.2)
        c.SetLogy(1)
        c.SaveAs(outputDir+"trim_mean_corrected_1D_separate_log.png")
        c.SaveAs(outputDir+"trim_mean_corrected_1D_separate_log.pdf")

        h_trim_corrected_1D.SetStats(0)
        h_trim_corrected_1D.GetXaxis().SetLabelSize(0.025)
        h_trim_corrected_1D.Draw()
        c.SaveAs(outputDir+"trim_mean_corrected_1D.pdf")
        c.SaveAs(outputDir+"trim_mean_corrected_1D.png")
        c.SetLogy(1)
        c.SaveAs(outputDir+"trim_mean_corrected_log_1D.pdf")
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
        
        self.avgGasGainDict = {}
        for histKey,sumHist in histDict.iteritems():
            trimSumHist = self.makeTrimHist(sumHist)
            self.avgGasGainDict[histKey] = trimSumHist
            print "Trimmed mean with "+histKey+": "+str(trimSumHist.GetMean())

    def makePosDepGasGain(self,collector,outputDir):
        outDir = outputDir+"/PosDepGasGain/"
        if not os.path.exists(os.path.abspath(outDir)):
            os.makedirs(os.path.abspath(outDir))
        
        c = ROOT.TCanvas()
        for isample,sample in enumerate(collector.samples):
            selectedList = [key for key in collector.fileDict[sample].GetListOfKeys() if key.GetName().startswith("SumQY") ]
            nBins = len(selectedList)
            summaryHist = ROOT.TH1D(sample+"_PosDepGasGain","",nBins,-0.5,nBins-0.5)
            for ikey,key in enumerate(selectedList):
                if not key.GetName().startswith("SumQY"): continue
                hist = collector.getObj(sample,key.GetName())
                trimHist = self.makeTrimHist(hist)
                trimMean = trimHist.GetMean()
                summaryHist.SetBinContent(ikey+1,trimMean)
                if trimHist.Integral():
                    summaryHist.SetBinError(ikey+1,trimHist.GetRMS()/math.sqrt(trimHist.Integral()))
                summaryHist.GetXaxis().SetBinLabel(ikey+1,key.GetName().split("_")[1])
                summaryHist.SetStats(0)
            summaryHist.Draw()
            c.SaveAs(outDir+"/"+sample+".png")
            c.SaveAs(outDir+"/"+sample+".pdf")

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
                if "Loc" in key.GetName(): continue
                if "SumQX" in key.GetName() or "SumQY" in key.GetName(): continue
                rhidList = self.convert_rhid(key.GetName().replace("SumQ",""))
                detidStr =  self.convert_key(rhidList)
                if detidStr in self.disHVList or detidStr in self.weakHVList: continue
                hist = collector.getObj(sample,key.GetName())
                histDict[sample].Fill(hist.GetEntries())
            histDict[sample].Draw()
            c.SaveAs(outDir+"/"+sample+".png")
        self.EntriesHistDict = histDict

    def makeLocHist(self,collector,outputDir):
        outDir = outputDir+"/LocXY/"
        if not os.path.exists(os.path.abspath(outDir)):
            os.makedirs(os.path.abspath(outDir))

        c = ROOT.TCanvas()
        for var in ["XLoc","YLoc"]:
            for isample,sample in enumerate(collector.samples):
                hist = collector.getObj(sample,var+sample)
                hist.Draw()
                c.SaveAs(outDir+"/"+var+"-"+sample+".png")

    def __call__(self,collector):

        outputDir = self.outputDir
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))

        collector.samples.sort()
        #self.makeLocHist(collector,outputDir)
        #self.makeEntriesHist(collector,outputDir)
        self.makeAvgGasGain(collector)
        #self.makePosDepGasGain(collector,outputDir)
        self.make1DSummaryHist(collector,outputDir)

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
        

