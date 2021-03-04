import copy
from Core.BaseDataset import BaseDataset

class Dataset(BaseDataset):
    def __init__(self,name,componentList,isMC=False,isSignal=False):
        self.name = name
        self.componentList = componentList
        self.isMC = isMC
        self.isData = not isMC
        self.isSignal = isSignal

    def makeComponents(self):
        componentList = []
        for icmp,cmp in enumerate(self.componentList):
            tmpCmp = copy.deepcopy(self)
            tmpCmp.componentList = [cmp]
            tmpCmp.name = self.name+"_"+str(icmp)
            tmpCmp.fileName = cmp.fileName
            tmpCmp.treeName = cmp.treeName
            tmpCmp.maxEvents = cmp.maxEvents
            tmpCmp.parent = self
            tmpCmp.fdConfigs = cmp.fdConfigs
            tmpCmp.fdFiles = cmp.fdFiles
            tmpCmp.fdTrees = cmp.fdTrees
            tmpCmp.beginEntry = cmp.beginEntry
            tmpCmp.reportInterval = cmp.reportInterval
            componentList.append(tmpCmp)
        return componentList
