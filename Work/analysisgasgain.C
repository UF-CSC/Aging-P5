#include "TMath.h"
#include "TBranch.h"  
#include "TTree.h"
#include "TFile.h"
#include "string"
#include "sstream"
#include <vector>
#include <iostream>
#include "TClassTable.h"
#include "TROOT.h"
#include "TString.h"

void analysisgasgain(Int_t fstat,Int_t fprint,string ntuplename,string histroot) {
  
  gSystem->Load("../Src/HistMan_cxx.so");
  gSystem->Load("../Src/AnalysisGasGain_cxx.so");

  
  HistMan *histos = new HistMan();
  AnalysisGasGain *anl=new AnalysisGasGain();
  ntuplename.replace(ntuplename.begin(),ntuplename.begin()+9,"");
  string prefix = "root://cmsio5.rc.ufl.edu/";
  ntuplename = prefix+ntuplename;
  cout << ntuplename <<endl;
  anl->Setup(fstat,fprint);
  anl->SetupTree(ntuplename,histroot);
  anl->Analyze(histos);

  delete anl;
 
 }
