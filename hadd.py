from Config.Chamber import ChamberList

import sys,os,glob

inputDir = sys.argv[1]
outputDir = sys.argv[2]

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

for chamberName in ChamberList:
    wildCardStr = inputDir+"/*"+chamberName+"*"
    os.system('hadd -f '+outputDir+"/"+chamberName+".root "+wildCardStr)
