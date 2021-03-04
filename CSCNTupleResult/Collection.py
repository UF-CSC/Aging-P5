
import ROOT

class Object(object):
    """Class that allows seeing a set branches plus possibly an index as an Object"""
    def __init__(self,event,objName,index):
        self._event   = event
        self._objName = objName+"_"
        self._index   = index
        pass

    def __getattr__(self,quantity):
        if quantity != "label":
            return getattr(self._event,self._objName+quantity)[self._index]
        else:
            return self._objName[:-1] 

class Collection(object):
    def __init__(self,event,objName,lenStr):
        self._event   = event   
        self._objName = objName
        self._lenStr = lenStr
        self._phyDict = {}

    def __getitem__(self,index):
        if index >= len(self):
            raise IndexError
        else:
            if index not in self._phyDict:
                self._phyDict[index] = Object(self._event,self._objName,index)
            return self._phyDict[index]

    def __len__(self):
        # probably a hack
        return getattr(self._event,self._objName+"_"+self._lenStr)[0]
