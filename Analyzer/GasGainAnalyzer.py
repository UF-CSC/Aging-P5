from Core.Module import Module

from Core.CSCNTupleResult.Collection import Collection

from Config.Chamber import ChamberDict

import ROOT,os

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
    def __init__(self,name):
        super(SkimTreeGasGainPlotter,self).__init__(name)
    
    def begin(self):
        self.writer.book("SumQ"+self.dataset.name,"TH1D",self.dataset.name,"",3000,0,3000)
    
    def analyze(self,event):
        self.writer.objs["SumQ"+self.dataset.name].Fill(event._rhsumQ_RAW[0])
        rhidStr = str(event._rhid[0])
        if "SumQ"+rhidStr not in self.writer.objs:
            self.writer.book("SumQ"+rhidStr,"TH1D","SumQ"+rhidStr,"",3000,0,3000)
        self.writer.objs["SumQ"+rhidStr].Fill(event._rhsumQ_RAW[0])
        return True
