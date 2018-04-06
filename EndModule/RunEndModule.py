import os,ROOT,math

ROOT.gROOT.SetBatch(ROOT.kTRUE)

class SkimTreeRunEndModule(EndModule):
    def __init__(self,outputDir):
        self.outputDir = outputDir

    def __call__(self,collector):
        outputDir = self.outputDir
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))
        
