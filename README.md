# CSCAgeingP5

## Origin
Code inherented from Laurent Thomas, git repo [here](https://github.com/lathomas/CSCAgeingP5)

## Instruction
CSC ageing studies on P5 data

### Setup 

The following works from the IHEPA machines and requires a CMSSW release to be installed.
It was tested under CMSSW_8_0_27.
 
 ```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_8_0_27 
cd CMSSW_8_0_27/src
cmsenv 
git clone https://github.com/lathomas/CSCAgeingP5  
```

In CSCAgeingP5/Work, edit the script_mysetup to define some global variables such as the folder you will be working on and the folder for outputs. 

Then run: 

```
source  script_mysetup
```

Finally, you will need a valid GRID certificate (to access data on HPC from IHEPA)

```
voms-proxy-init --voms cms --valid 168:00 
```

2. Input files 
- This study is based on ROOT ntuples produced by Hualin Mei using the UF rootmaker on the HPC cluster:

```
/cms/data/store/user/hmei/rootfiles_2017/CSCNtuples_2016SingleMu_BCDEFGH_promptReco/SingleMuon/
```

So far only 2016 data were processed. 

Unfortunately these data are not directly visible from IHEPA.
To list all the inputs from a given run era 	  in a text file, you need to ssh to HPC: \

```
ssh user@cmsio2.rc.ufl.edu
ls /cms/data/store/user/hmei/rootfiles_2017/CSCNtuples_2016SingleMu_BCDEFGH_promptReco/SingleMuon/crab_SingleMuon_Run2016G-PromptReco-v1/170322_174419/000*/*.root  >  
```

and copy SingleMuReco_2016G_list.txt to your Work/ folder in IHEPA. 


3. Producing small trees with information relevant for the ageing study 
This is performed through separated scripts for each run era so that several of them can be run at the same time. 
The code itself is in the class AnalysisGasGain. 
Before to run the script, compile and link the HistMan and AnalysisGasGain code (if you made changes in it or run it first time) by corresponding macros build_histman.C and build_analysisgasgain.C (being in folder Src):

```
root -b -q  build_histman.C // to compile and link histogram manager HistMan
root -b -q build_analysisgasgain.C // to compile and link AnalysisGasGain (this takes a few minutes)
```

You can then test the code by running on a single file: 

```
root -l -b -q ../Src/HistMan_cxx.so ../Src/AnalysisGasGain_cxx.so analysisgasgain.C\(0,0,\"/cms/data/store/user/hmei/rootfiles_2017/CSCNtuples_2016SingleMu_BCDEFGH_promptReco/SingleMuon/crab_SingleMuon_Run2016H-PromptReco-v3/170322_174443/0000/SingleMuon_Run2016H-PromptReco-v3_115.root\",\"myoutput.root\"\) 
```

One file is produced for each station/ring/HV segment separately. They all contain a tree where each event corresponds to a rechit. 
(N.B. one can probably reduce the file size by a significant amount by changing the format and saving multiple hits in the same event...)
Two important variables here are 

```
_rhsumQRAW: ADC charge as measured during the data taking
_rhsumQ: ADC charge, undoing the HV changes made in the latest data. (see: UncorrGasGain_HVInitial2016 in 
```

Running on a full run era will take time ( O(10h) ). 
This can be done using for example: 

```
mkdir $OUT/2016G
source script_gasgain_rung
```

The outputs will be stored in the directory defined in script_mysetup 
All output files should then be merged into a single one for each station/ring/HV segment: (e.g. "TOTALME21HV1.root"). 

4. Extracting Gas gain dependency. 
This is done with a C++ class ( ProduceHistosPerChannel) 
Assuming you have the file TOTALME21HV1.root in the subfolder Work, do: 

```
root -l -b 
.L ../Src/ProduceHistosPerChannel.C++
ProduceHistosPerChannel d
d.Loop("TOTALME21HV1") //No ".root" extension 
```

The resulting output file will then contain histograms with all fits, as well as the slope distribution for each variable studied in a single histogram. 
