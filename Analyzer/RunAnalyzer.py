from Core.Module import Module

from Core.CSCNTupleResult.Collection import Collection

from Config.Chamber import ChamberDict

import ROOT,os

class RunPlotter(Module):
    def begin(self):
        self.writer.book("runDict","dict")        

    def analyze(self,event):
        if event.Run[0] not in self.runDict:
            self.writer.objs["runDict"][event.Run[0]] = 0
        self.writer.objs["runDict"][event.Run[0]] += 1
        return True
 
class SkimTreeRunPlotter(Module):
    def begin(self):
        self.writer.book("runDict","dict")        

    def analyze(self,event):
        if event._runNb[0] not in self.writer.objs["runDict"]:
            self.writer.objs["runDict"][event._runNb[0]] = 0
        self.writer.objs["runDict"][event._runNb[0]] += 1
        return True
 
        
