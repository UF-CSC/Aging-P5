from Core.CSCNTupleResult.ComponentProcessor import ComponentProcessor
from Core.CSCNTupleResult.ProgressReportWriter import ProgressReportWriter
from Core.NanoAODResult.FileInfo import prefix_UFTier2
import ROOT,os,uuid

class TreeProducer(ComponentProcessor):
    def __init__(self,component,outputPathTemplate):
        self.prefix = prefix_UFTier2
        self.outputPathTemplate = outputPathTemplate
        self.component = component
        self.progressReportWriter = ProgressReportWriter()
        self.taskid = uuid.uuid4()

    def __call__(self,progressReporter=None):
        ROOT.gSystem.Load(os.environ["BASE_PATH"]+"/Src/HistMan_cxx.so")
        ROOT.gSystem.Load(os.environ["BASE_PATH"]+"/Src/AnalysisGasGain_cxx.so")
        anl = ROOT.AnalysisGasGain()
        histMan = ROOT.HistMan()
        inputPath = self.prefix+self.component.path.replace("/cms/data","")
        outputPath = self.outputPathTemplate
        self._reportProgress(progressReporter,0,2)
        anl.Setup(0,0)
        anl.SetupTree(inputPath,self.outputPathTemplate%self.component.name)
        anl.Analyze(histMan)
        self._reportProgress(progressReporter,1,2)

    def _reportProgress(self, progressReporter, event, total):
        if progressReporter is None: return
        report = self.progressReportWriter.write(self.taskid, self.component.name,event,total)
        progressReporter.report(report)
