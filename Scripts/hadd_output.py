from Config.Chamber import ChamberList

import os,ROOT

inputDir = "/raid/raid7/lucien/CSC/GasGain/Log/2018-05-07/"
outputDir = "/raid/raid7/lucien/CSC/GasGain/Log/2018-05-17/"
fileName = "test1.root"

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

dirs_to_hadd = os.listdir(inputDir)

for chamber in ChamberList:
    chamberDir = outputDir+"/"+chamber+"/"
    if not os.path.exists(os.path.abspath(chamberDir)):
        os.makedirs(chamberDir)

    fileList = [inputDir+dir_to_hadd+"/"+chamber+"/"+fileName for dir_to_hadd in dirs_to_hadd]
    fileList.sort()

    cmdStr = 'hadd -f '+chamberDir+fileName+" "+" ".join(fileList)
    os.system(cmdStr)
