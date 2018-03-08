# alphatwirl
from Core.ProgressBar import ProgressBar,ProgressReport,ProgressMonitor,BProgressMonitor
from Core.Concurrently import CommunicationChannel,CommunicationChannel0
from Core.HeppyResult import ComponentLoop

from Core.CSCNTupleResult.Component import Component

from Core.Utils.git import getGitDescribe,getGitDiff

from Analyzer.TreeProducer import TreeProducer

# Standard package
import imp,sys,os

cfgFileName             = sys.argv[1]
file                    = open( cfgFileName,'r')
cfg                     = imp.load_source( 'UFCSC.__cfg_to_run__', cfgFileName, file)

nCores                  = cfg.nCores
componentList           = cfg.componentList
disableProgressBar      = cfg.disableProgressBar
outputPathTemplate      = cfg.outputPathTemplate
outputDir               = os.path.dirname(cfg.outputPathTemplate)

progressBar = ProgressBar()

if nCores != 1:
    progressMonitor      = BProgressMonitor(progressBar)
    communicationChannel = CommunicationChannel(nCores,progressMonitor)
else:
    progressMonitor      = ProgressMonitor(progressBar)
    communicationChannel = CommunicationChannel0(progressMonitor)
    pass
    
if not disableProgressBar: progressMonitor.begin()
communicationChannel.begin()

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

gitFile        = os.path.join(outputDir,"gitDetails.txt")
gitVerboseFile = os.path.join(outputDir,"gitVerboseDetails.txt")
with open(gitFile,'w') as f:
    f.write(getGitDescribe())

with open(gitVerboseFile,'w') as f:
    f.write(getGitDiff())

print "\nLoading samples:\n"

for component in componentList:
    processor       = TreeProducer(component,outputPathTemplate)
    communicationChannel.put(processor)

communicationChannel.receive()

print "\nEnd Running\n"
if not disableProgressBar: progressMonitor.end()
communicationChannel.end()
