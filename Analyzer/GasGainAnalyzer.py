from Core.Module import Module

from Core.CSCNTupleResult.Collection import Collection

from Config.Chamber import *

import ROOT,os
from bisect import bisect_left

class GasGainPlotter(Module):
    def __init__(self,name):
        super(GasGainPlotter,self).__init__(name)
    
    def begin(self):
        ROOT.gSystem.Load(os.environ["BASE_PATH"]+"/Src/HistMan_cxx.so")
        ROOT.gSystem.Load(os.environ["BASE_PATH"]+"/Src/AnalysisGasGain_cxx.so")
        self.anl = ROOT.AnalysisGasGain()
        self.anl.Setup(0,0)
        for chamberKey,chamberName in ChamberDict.iteritems():
            self.writer.book("SumQ"+str(chamberKey),"TH1D",chamberName,"",3000,0,3000)
        self._cacheDict = {}
    
    def analyze(self,event):
        recHits = Collection(event,"recHits2D","nRecHits2D")
        for recHit in recHits:
            hvsgm = self.anl.doHVsegment(recHit.localY,recHit.ID_station,recHit.ID_ring,recHit.ID_layer)
            if hvsgm == 0: continue
            if (recHit.ID_station,recHit.ID_ring,hvsgm) not in self._cacheDict:
                self._cacheDict[(recHit.ID_station,recHit.ID_ring,hvsgm)] = self.anl.GetRegionIdx(recHit.ID_station,recHit.ID_ring,hvsgm)
            self.writer.objs["SumQ"+str(self._cacheDict[(recHit.ID_station,recHit.ID_ring,hvsgm)])].Fill(recHit.SumQ)
        return True

class SkimTreeGasGainPlotter(Module):
    def begin(self):
        self.writer.book("SumQ"+self.dataset.name,"TH1D",self.dataset.name,"",3000,0,3000)

    def analyze(self,event):
        self.writer.objs["SumQ"+self.dataset.name].Fill(event._rhsumQ_RAW[0])
        rhidStr = str(event._rhid[0])
        if self.dataset.name == "ME11": rhidStr = rhidStr[0:2]+"1"+rhidStr[3:]
        if "SumQ"+rhidStr not in self.writer.objs:
            self.writer.book("SumQ"+rhidStr,"TH1D","SumQ"+rhidStr,"",3000,0,3000)
        self.writer.objs["SumQ"+rhidStr].Fill(event._rhsumQ_RAW[0])
        return True

class SkimTreePositionPlotter(Module):
    def __init__(self,name,y_seg_dict):
        super(SkimTreePositionPlotter,self).__init__(name)
        self.y_seg_dict = y_seg_dict
        self.nYBins = 5
    
    def begin(self):
        self.binEdgeDict = {}
        self.chamberType = self.dataset.name[0:4]
        lowEdge,highEdge = self.y_seg_dict[self.chamberType]
        self.yBinEdges = [lowEdge+i*(highEdge-lowEdge)/self.nYBins for i in range(0,self.nYBins+1)]
        for ybin in self.yBinEdges:
            name = "PosDepSumQ"+"_YLoc"+str(int(ybin))+"_"+self.chamberType
            self.writer.book(name,"TH1D",name,"",3000,0,3000)
    
    def analyze(self,event):
        #index = bisect_left(self.x_segments,event._xloc[0])
        #if xindex == len(self.x_segments): xindex -= 1
        #self.writer.objs["XLoc"+"_"+str(self.x_segments[xindex])+"_"+self.dataset.name].Fill(event._xloc[0])
        yindex = bisect_left(self.yBinEdges,event._yloc[0])
        if yindex == len(self.yBinEdges): yindex -= 1
        self.writer.objs["PosDepSumQ"+"_YLoc"+str(int(self.yBinEdges[yindex]))+"_"+self.chamberType].Fill(event._rhsumQ_RAW[0])
        return True



