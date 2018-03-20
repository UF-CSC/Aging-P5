#include "AnalysisGasGain.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <sstream>
#include "TTree.h"
#include "TFile.h"
#include "TLorentzVector.h"
#include <limits>
#include <map>
#include "pressurecsc.h"

#include "IntegrateLumi.h"

#include "ChargeORIGandInstL.h"
ClassImp(AnalysisGasGain)

std::map <Int_t, Int_t>     m_Run_usedevents,m_Run_usedhits;
std::map <Int_t, Int_t>     m_RunEvent;
std::map <Int_t, UInt_t>    m_RunStart;
std::map <Int_t, UInt_t>    m_RunEnd;

std::map <Int_t, Int_t>     m_ordstatring;
std::map <Int_t, Int_t>     m_nRecHitlayer;
std::map <Int_t, Int_t>     m_nRecHitchamber;

std::map <Int_t, Int_t>     m_nRecHitlayerME14;
std::map <Int_t, std::vector <Double_t> > 
                            m_RecHitlayerME14_final;
std::map <UInt_t, std::vector <Double_t> >  
                            m_cscSegments_recHitRecordX,
                            m_cscSegments_recHitRecordY;
std::map <Int_t, Int_t>     m_nsegments_chamber;
std::map <UInt_t, std::vector <Double_t> >  
                            m_muon_segm;
std::map <Int_t, std::vector <Double_t> >  
                            m_Single_cscSegments_recHitRecordX,
                            m_Single_cscSegments_recHitRecordY;
std::map <Int_t, std::vector <Double_t> >  
                            m_cscSegments_single_trk_recHitRecord,
                            m_cscSegments_single_trk_recHitRecord_final;

int minhitpersegment = 5;
AnalysisGasGain::AnalysisGasGain() { }

AnalysisGasGain::~AnalysisGasGain() { }

/* **************************** Setup ************************************* */
void AnalysisGasGain::SetupTree(string inp,string out)
{
  ntuplename=inp;
  histrootname=out;
  // SetupPrint();
  for(int i = 0; i <32;i++){
    TString treename =GetRegionName(i);
    TString filetreelocation = (TString) out;
    filetreelocation.ReplaceAll(".root",treename+"_tree.root");
    myoutfilefortree[i] = new TFile(filetreelocation,"recreate"); 
    
    outputtree[i] = new TTree("tree","tree");
    outputtree[i]->Branch("_passZmumusel",   &passZmumusel,   "_passZmumusel/O");
    outputtree[i]->Branch("_eventNb",   &_eventNb,   "_eventNb/l");
    outputtree[i]->Branch("_runNb",   &_runNb,   "_runNb/l");
    outputtree[i]->Branch("_lumiBlock",   &_lumiBlock,   "_lumiBlock/l");
    outputtree[i]->Branch("_rhid",&_rhid,"_rhid/I");
    outputtree[i]->Branch("_stationring",&_stationring,"_stationring/I");
    outputtree[i]->Branch("_rhsumQ",&_rhsumQ,"_rhsumQ/D");
    outputtree[i]->Branch("_rhsumQ_RAW",&_rhsumQ_RAW,"_rhsumQ_RAW/D");
    outputtree[i]->Branch("_HV",&_HV,"_HV/D");
    outputtree[i]->Branch("_pressure",&_pressure,"_pressure/D");
    outputtree[i]->Branch("_temperature",&_temperature,"_temperature/D");
    outputtree[i]->Branch("_instlumi",&_instlumi,"_instlumi/D");
    outputtree[i]->Branch("_integratelumi",&_integratelumi,"_integratelumi/D");
    outputtree[i]->Branch("_timesecond",&_timesecond,"_timesecond/i") ;
    outputtree[i]->Branch("_n_PV",&_n_PV,"_n_PV/I");
    outputtree[i]->Branch("_bunchcrossing",&_bunchcrossing,"_bunchcrossing/I");
    outputtree[i]->Branch("_etamuon",&_etamuon,"_etamuon/D");
    outputtree[i]->Branch("_phimuon",&_phimuon,"_phimuon/D");
    outputtree[i]->Branch("_ptmuon",&_ptmuon,"_ptmuon/D");
  }
}

void AnalysisGasGain::Setup(Int_t fstat,Int_t fprint)
{
  flag_stat=fstat;
  flag_print=fprint;

  Int_t strng[10]={11,12,13,14,21,22,31,32,41,42};
  m_ordstatring.clear();
  for(Int_t i=0;i<10;i++) {
    Int_t key=strng[i];
    if(m_ordstatring.find(key)==m_ordstatring.end())
      m_ordstatring[key]=i+1; // just for order numeration to use in hists
  }
 
  for(Int_t i=0;i<3;i++) zero3.push_back(0.0);
  for(Int_t i=0;i<6;i++) zero6.push_back(-999.0);
  for(Int_t i=0;i<5;i++) zero5.push_back(0.0);
// Calculate and store Yloc boundaries of the HV segments in CSC
//**************************************************
//CSC        ME12   ME13   ME21  ME31  ME41  ME234/2 
//# HV segm   3      3      3     3     3     5
//**************************************************

 const Int_t ntype=6;
 const Int_t nsegm3=3;
 const Int_t nsegm5=5;

 // Al frame height, (cm, between outer edges)
 Float_t h[ntype]={189.4, 179.3, 204.6, 184.6, 164.7, 338.0};

 // dFtoAP-distance from the narrow edge of the Al Frame to the Alignment Pin
 Float_t dftoap=3.49; // cm

 // Distances (mm) of the first (*Low) and last (*High) thick wires 
 // of the HV segment from alignment pin 
 Float_t dapme12Low[nsegm3] = { 28.5,  594.3, 1251.8},   
         dapme12High[nsegm3]= {572.2, 1229.7, 1776.6},

	 dapme13Low[nsegm3] = { 28.5,  645.3, 1151.3},   
	 dapme13High[nsegm3]= {623.1, 1129.2, 1673.2}, 

	 dapme21Low[nsegm3] = { 28.7,  724.3, 1335.7},   
	 dapme21High[nsegm3]= {702.5, 1313.9, 1928.4}, 

	 dapme31Low[nsegm3] = { 28.4,  536.9, 1135.8},   
	 dapme31High[nsegm3]= {515.0, 1114.0, 1728.5},

	 dapme41Low[nsegm3] = { 30.4,  538.9, 1038.0},   
	 dapme41High[nsegm3]= {517.0, 1016.1, 1527.7},

	 dapme234_2Low[nsegm5]={ 28.7,   847.4, 1454.3, 2061.3, 2668.2},
	 dapme234_2High[nsegm5]={825.3, 1432.2, 2039.1, 2646.1, 3262.5};

 // Calculate Y loc for HV segment boundaries (Low and High).
 // Y loc = 0 is in the symmetry center of Al frame, e.g. at h[]/2.0
 for(Int_t i=0;i<nsegm3;i++) {
   me12YlocHVsgmLow[i]    = -h[0]/2.0+dftoap+dapme12Low[i]/10.0;
   me12YlocHVsgmHigh[i]   = -h[0]/2.0+dftoap+dapme12High[i]/10.0; 

   me13YlocHVsgmLow[i]    = -h[1]/2.0+dftoap+dapme13Low[i]/10.0;
   me13YlocHVsgmHigh[i]   = -h[1]/2.0+dftoap+dapme13High[i]/10.0;

   me21YlocHVsgmLow[i]    = -h[2]/2.0+dftoap+dapme21Low[i]/10.0;
   me21YlocHVsgmHigh[i]   = -h[2]/2.0+dftoap+dapme21High[i]/10.0;

   me31YlocHVsgmLow[i]    = -h[3]/2.0+dftoap+dapme31Low[i]/10.0;
   me31YlocHVsgmHigh[i]   = -h[3]/2.0+dftoap+dapme31High[i]/10.0; 
 
   me41YlocHVsgmLow[i]    = -h[4]/2.0+dftoap+dapme41Low[i]/10.0;
   me41YlocHVsgmHigh[i]   = -h[4]/2.0+dftoap+dapme41High[i]/10.0; 
 }

 for(Int_t i=0;i<nsegm5;i++) {
   me234_2YlocHVsgmLow[i]    = -h[5]/2.0+dftoap+dapme234_2Low[i]/10.0;
   me234_2YlocHVsgmHigh[i]   = -h[5]/2.0+dftoap+dapme234_2High[i]/10.0; 
 }
  // end of Y loc HV segment boundaries calculations
}

/* *********************** SetupPrint ************************************* */

void AnalysisGasGain::SetupPrint() {

  cout<<" "<<endl;
  cout<<ntuplename.c_str()<<endl;
  cout<<histrootname.c_str()<<endl;
  cout<<"flag_stat flag_print "<<flag_stat<<" "<<flag_print<<endl;
  cout<<""<<endl;
}

/* *********************** Find HV segment ***********************************/
Int_t  AnalysisGasGain::doHVsegment(Float_t yloc,Int_t stn,Int_t rng,Int_t layer)
{
  // Use local Y to find HV segment number.

  Int_t segment=0; //Define Segment # as 0 if not found

  const Int_t nsegm3=3;
  const Int_t nsegm5=5;

  if(stn==1 && (rng==1 || rng==4)) segment=layer; // ME11 or ME14

  if(stn==1 && rng==2) { //ME12
    for(Int_t i=0;i<nsegm3; i++)
    if((yloc >= me12YlocHVsgmLow[i]) && (yloc <= me12YlocHVsgmHigh[i]))
      segment=i+1;
  }

  if(stn==1 && rng==3) { //ME13
    for(Int_t i=0;i<nsegm3; i++)
    if((yloc >= me13YlocHVsgmLow[i]) && (yloc <= me13YlocHVsgmHigh[i]))
      segment=i+1;
  }

  if(stn==2 && rng==1) { //ME21
    for(Int_t i=0;i<nsegm3; i++)
    if((yloc >= me21YlocHVsgmLow[i]) && (yloc <= me21YlocHVsgmHigh[i]))
      segment=i+1;
  }

  if(stn==3 && rng==1) { //ME31
    for(Int_t i=0;i<nsegm3; i++)
    if((yloc >= me31YlocHVsgmLow[i]) && (yloc <= me31YlocHVsgmHigh[i]))
      segment=i+1;
  }

  if(stn==4 && rng==1) { //ME41
    for(Int_t i=0;i<nsegm3; i++)
    if((yloc >= me41YlocHVsgmLow[i]) && (yloc <= me41YlocHVsgmHigh[i]))
      segment=i+1;
  }
 
  if((stn==2 || stn==3 || stn==4) && rng==2) { //ME234/2 
    for(Int_t i=0;i<nsegm5; i++)
    if((yloc >= me234_2YlocHVsgmLow[i]) && (yloc <= me234_2YlocHVsgmHigh[i]))
      segment=i+1;
  }

  return segment;
}

/* ************************** Analyze ************************************* */

void AnalysisGasGain::Analyze(HistMan *histos) {

  CycleTree(histos);
  histos->ClearHistMaps();
  for(int i = 0; i<32;i++){
  myoutfilefortree[i]->cd();
  outputtree[i]->Write();
  myoutfilefortree[i]->Close();
  }
}

/* *******************    GetME14RecHits ********************************** */

void AnalysisGasGain::GetME14RecHits(HistMan* histos) {

for(Int_t irechit=0;irechit<frecHits2D_nRecHits2D;irechit++) {            

     Int_t endcap=frecHits2D_ID_endcap[irechit];
     Int_t station=frecHits2D_ID_station[irechit];
     Int_t ring=frecHits2D_ID_ring[irechit]; 
     Int_t chamber=frecHits2D_ID_chamber[irechit];
     Int_t layer=frecHits2D_ID_layer[irechit];
     Double_t sumq=frecHits2D_SumQ[irechit];

     Int_t key_layer=100000*endcap+10000*station+1000*ring+10*chamber+layer;
     Int_t key_chmb=10000*endcap+ 1000*station+ 100*ring+chamber;
      
     if(m_nRecHitlayer.find(key_layer)== m_nRecHitlayer.end())
       m_nRecHitlayer[key_layer]=0;
     m_nRecHitlayer[key_layer]= m_nRecHitlayer[key_layer]+1;
     if(m_nRecHitchamber.find(key_chmb)== m_nRecHitchamber.end())
       m_nRecHitchamber[key_chmb]=0;
     m_nRecHitchamber[key_chmb]= m_nRecHitchamber[key_chmb]+1;
     
     if(station==1 && ring==4 && sumq > 0.0) { //ME14
       if(m_nRecHitlayerME14.find(key_layer)== m_nRecHitlayerME14.end())
         m_nRecHitlayerME14[key_layer]=0;
       m_nRecHitlayerME14[key_layer]=m_nRecHitlayerME14[key_layer]+1;
     }
 } // end of for(Int_t irechit=0;irechit<frecHits2D_nRecHits2D;...)

 for(std::map<Int_t,Int_t>::iterator It=m_nRecHitlayer.begin(); It!= m_nRecHitlayer.end();++It) {
   Float_t nhits=(Float_t)(*It).second;
    histos->fill1DHist(nhits,"nhits_per_layer","","# of RecHit2D per layer","Entries",4,100,0.0,100.0,1.0,"Test");
 }
 for(std::map<Int_t,Int_t>::iterator It=m_nRecHitchamber.begin(); It!= m_nRecHitchamber.end();++It) {
   Float_t nhits=(Float_t)(*It).second;
    histos->fill1DHist(nhits,"nhits_per_chamber","","# of RecHit2D per chamber","Entries",4,1000,0.0,1000.0,1.0,"Test");
 }

 // now store the first hit from 3 hits of ME14 (SumQ is the same in all 3)
 // into final map m_RecHitlayerME14_final
 
 for(Int_t irechit=0;irechit<frecHits2D_nRecHits2D;irechit++) {

     Int_t endcap=frecHits2D_ID_endcap[irechit];
     Int_t station=frecHits2D_ID_station[irechit];
     Int_t ring=frecHits2D_ID_ring[irechit];
     Int_t chamber=frecHits2D_ID_chamber[irechit];
     Int_t layer=frecHits2D_ID_layer[irechit];
     Double_t xloc=frecHits2D_localX[irechit];
     Double_t yloc=frecHits2D_localY[irechit];
     Double_t sumq=frecHits2D_SumQ[irechit];

     if(station==1 && ring==4 && sumq > 0.0) { //ME14
       Int_t key_layer=100000*endcap+10000*station+1000*ring+10*chamber+layer;
       if(m_nRecHitlayerME14.find(key_layer)== m_nRecHitlayerME14.end())
         cout<<"Error, no m_nRecHitlayerME14 for key "<<key_layer<<endl;
       if(m_nRecHitlayerME14.find(key_layer)!= m_nRecHitlayerME14.end())   
         if(m_nRecHitlayerME14[key_layer]==3){// From what I understand this ensures there are only 3 hits (i.e. 3 times the same hit) in a given layer. (???).
           if(m_RecHitlayerME14_final.find(key_layer)== m_RecHitlayerME14_final.end()) {
	     m_RecHitlayerME14_final[key_layer]=zero6;
	     m_RecHitlayerME14_final[key_layer][0]=xloc;
             m_RecHitlayerME14_final[key_layer][1]=yloc;
             m_RecHitlayerME14_final[key_layer][2]=sumq;
             m_RecHitlayerME14_final[key_layer][3]=999.;
             m_RecHitlayerME14_final[key_layer][4]=999.;
             m_RecHitlayerME14_final[key_layer][5]=999.;
	   }
	 } // end of if(m_nRecHitlayerME14[key_layer]==3)
     }  // end of  if(station==1 && ring==4 && sumq > 0.0)
 }  // end of for(Int_t irechit=0;irechit<frecHits2D_nRecHits2D

}

/* ******************** GetSegments (tracking segments)***********************/

void AnalysisGasGain::GetSegments(HistMan* histos) {
       histos->fill1DHist((Float_t)fcscSegments_recHitRecord_endcap->size(),"all_segments_per_event","","All segments per event","Entries",4,100,0.0,100.0,1.0,"Test");

     Int_t nhits_segm_event=0;
     for(UInt_t i=0;i<fcscSegments_recHitRecord_endcap->size();i++) {

        if(i<100) { // limit 100 segments per event for key_segment

	  histos->fill1DHist((Float_t)(*fcscSegments_recHitRecord_endcap)[i].size(),"all_hits_per_segment","","All hits per segment","Entries",4,10,0.0,10.0,1.0,"Test");
          // use segments with hits in 4-6 layers only
	  
	  if((Int_t)(*fcscSegments_recHitRecord_endcap)[i].size() >= minhitpersegment ) {
	    
            for(UInt_t j=0;j<(*fcscSegments_recHitRecord_endcap)[i].size();j++) {
	    // here i-segment,j-hit
            Int_t endcap=(Int_t)(*fcscSegments_recHitRecord_endcap)[i][j];
            Int_t station=(Int_t)(*fcscSegments_recHitRecord_station)[i][j];
            Int_t ring=(Int_t)(*fcscSegments_recHitRecord_ring)[i][j];
            Int_t chamber=(Int_t)(*fcscSegments_recHitRecord_chamber)[i][j];
            Int_t layer=(Int_t)(*fcscSegments_recHitRecord_layer)[i][j];
            Double_t localX=(*fcscSegments_recHitRecord_localX)[i][j];
            Double_t localY=(*fcscSegments_recHitRecord_localY)[i][j];



            UInt_t key_segment=1000000*endcap+100000*station+10000*ring+100*chamber+i;
	    if(j==0) {
              nhits_segm_event=nhits_segm_event+(Int_t)(*fcscSegments_recHitRecord_endcap)[i].size();
              Int_t key_chamber=(Int_t)(key_segment/100);
              // count # of segments per chamber
              if(m_nsegments_chamber.find(key_chamber)==m_nsegments_chamber.end())
	        m_nsegments_chamber[key_chamber]=0;
	      m_nsegments_chamber[key_chamber]=m_nsegments_chamber[key_chamber]+1;
	    } // end of if(j==0)

            
            if(m_cscSegments_recHitRecordX.find(key_segment)==m_cscSegments_recHitRecordX.end()) {
            m_cscSegments_recHitRecordX[key_segment]=zero6;
            m_cscSegments_recHitRecordY[key_segment]=zero6;
	    }
            m_cscSegments_recHitRecordX[key_segment][layer-1]=localX;
            m_cscSegments_recHitRecordY[key_segment][layer-1]=localY;

	    } // end of  for(UInt_t j=0;j<fcscSegments_recHitRecord_endcap[i]
	  } // end of if segment has >=minhitpersegment layers in it
	}   // end of if there is < 100 segments
     } // end of for(UInt_t i=0;i<fcscSegments_recHitRecord_endcap->size();i++)
 
       histos->fill1DHist((float)nhits_segm_event,"segment_nhits_per_event","","Segment hits per event","Entries",4,1000,0.0,1000.0,1.0,"Test");
       histos->fill1DHist((Float_t)m_nsegments_chamber.size(),"CSCs_with_segments_per_event","","# of CSCs with segments per event","Entries",4,100,0.0,100.0,1.0,"Test");

     for(std::map<Int_t,Int_t>::iterator It=m_nsegments_chamber.begin(); It!= m_nsegments_chamber.end();++It) {
       Float_t nsegm=(*It).second;
       histos->fill1DHist((Float_t)nsegm,"segments_per_chamber","","Number of segments per chamber","Entires",4,100,0.0,100.0,1.0,"Test");
     }

     // Here make map of single (per chamber) segments 
     // m_Single_cscSegments_recHitRecordX,*Y[key_chamber] from 
     // m_cscSegments_recHitRecordX,*Y using m_nsegments_chamber[key_chamber]=1

     if(m_nsegments_chamber.size() > 0 ) {
     for(UInt_t i=0;i<fcscSegments_recHitRecord_endcap->size();i++) {
       if((Int_t)(*fcscSegments_recHitRecord_endcap)[i].size() >= minhitpersegment ) { 
        Int_t endcap=(Int_t)(*fcscSegments_recHitRecord_endcap)[i][0];
        Int_t station=(Int_t)(*fcscSegments_recHitRecord_station)[i][0];
        Int_t ring=(Int_t)(*fcscSegments_recHitRecord_ring)[i][0];
        Int_t chamber=(Int_t)(*fcscSegments_recHitRecord_chamber)[i][0];


        Int_t key_chmb=10000*endcap+1000*station+100*ring+chamber;

        //if(m_nsegments_chamber.find(key_chmb)==m_nsegments_chamber.end())
        //  cout<<"Error, no segments for key_chmb="<<key_chmb<<" event "<<fEvent<<endl;
        if(m_nsegments_chamber.find(key_chmb)!=m_nsegments_chamber.end()) {
          if(m_nsegments_chamber[key_chmb]==1) {
	    if(m_Single_cscSegments_recHitRecordX.find(key_chmb) == m_Single_cscSegments_recHitRecordX.end()) { 
	      UInt_t key_segment=1000000*endcap+100000*station+10000*ring+100*chamber+i;  
              if(m_cscSegments_recHitRecordX.find(key_segment)== m_cscSegments_recHitRecordX.end()) cout<<"Error: no m_cscSegments_recHitRecordX with key_segment="<<key_segment<<endl;
              if(m_cscSegments_recHitRecordX.find(key_segment)!= m_cscSegments_recHitRecordX.end()) { 
		m_Single_cscSegments_recHitRecordX[key_chmb]=m_cscSegments_recHitRecordX[key_segment];
		m_Single_cscSegments_recHitRecordY[key_chmb]=m_cscSegments_recHitRecordY[key_segment];

	      }  // end of if(m_cscSegments_recHitRecordX.find(key_segment)
	    }   // end of if(m_Single_cscSegments_recHitRecordX.find(key_chmb)
	  }  // end of if(m_nsegments_chamber[key_chmb]==1)
	}   // end of if(m_nsegments_chamber.find(key_chmb)!
       } // end of if((Int_t)(*fcscSegments_recHitRecord_endcap)[i].size() >=minhitpersegment )
     }  // end of for(UInt_t i=0;i<fcscSegments_recHitRecord_endcap->size()
     }  // end if(m_nsegments_chamber.size() > 0 
 
     if(m_Single_cscSegments_recHitRecordX.size() > 0) {
       histos->fill1DHist((Float_t)m_Single_cscSegments_recHitRecordX.size(),"single_segm_chambers_per_event","","Single segment chambers per event","Entries",4,100,0.0,100.0,1.0,"Test");

       Int_t nhits_single_segm_event=0;
       for(std::map<Int_t,std::vector <Double_t> >::iterator It=m_Single_cscSegments_recHitRecordX.begin(); It!= m_Single_cscSegments_recHitRecordX.end();++It) {
          Int_t key_chmb=(*It).first;
          for(Int_t i=0;i<6;i++) if(m_Single_cscSegments_recHitRecordX[key_chmb][i] > -999.0) nhits_single_segm_event++;
       }
       histos->fill1DHist((float)nhits_single_segm_event,"single_segm_rechits_per_event","","Single segment hits per event","Entries",4,100,0.0,100.0,1.0,"Test");
     }
}

/* ***********************  GetTracks ********************************* */

void AnalysisGasGain::GetTracks(HistMan* histos) {
     ostringstream ss;
     if(m_Single_cscSegments_recHitRecordX.size() > 0) {//There should be at least one single segment in a chamber

     Int_t trackne=0;  // non empty track counter, e.g. track with CSC segments
     for(UInt_t i=0;i<fmuons_cscSegmentRecord_nRecHits->size();i++) //Loop over muons
        if(i<10 && (*fmuons_cscSegmentRecord_nRecHits)[i].size() > 0) 
	 // i< 10 due to use in key for map
         trackne++;

     histos->fill1DHist((Float_t)trackne,"nonempty_tracks_per_event","","Number of non empty tracks per event","Entires",4,10,0.0,10.0,1.0,"Test");

     if(trackne == 1) { // use events with single muon track
     Int_t trackneindmx=0;

     for(UInt_t i=0;i<fmuons_cscSegmentRecord_nRecHits->size();i++) {
       if(i<10 && (*fmuons_cscSegmentRecord_nRecHits)[i].size() > 0   && (fmuons_Zcand[i] || fmuons_isomuondzdxy[i] )) {//Last part added by Laurent
	 // i< 10 due to use in key for map
          histos->fill1DHist((Float_t)(*fmuons_cscSegmentRecord_nRecHits)[i].size(),"segments_per_track","","Number of CSC segments per track","Entries",4,10,0.0,10.0,1.0,"Test");
         if((Int_t)i>trackneindmx) trackneindmx=(Int_t)i;

         Int_t segmindmx=0;
         for(UInt_t j=0;j<(*fmuons_cscSegmentRecord_nRecHits)[i].size();j++) {
           if(j<10) { // limited due to use in key for map
           if((Int_t)j>segmindmx) segmindmx=(Int_t)j;
           Int_t endcap=(Int_t)(*fmuons_cscSegmentRecord_endcap)[i][j];
           Int_t station=(Int_t)(*fmuons_cscSegmentRecord_station)[i][j];
           Int_t ring=(Int_t)(*fmuons_cscSegmentRecord_ring)[i][j];
           Int_t chamber=(Int_t)(*fmuons_cscSegmentRecord_chamber)[i][j];
           Double_t localX=(*fmuons_cscSegmentRecord_localX)[i][j];
           Double_t localY=(*fmuons_cscSegmentRecord_localY)[i][j];
           Double_t nlayers=(*fmuons_cscSegmentRecord_nRecHits)[i][j];
    
           UInt_t key_trksegm=1000000*endcap+100000*station+10000*ring+
                         100*chamber+10*i+j;
           Int_t key_chmb=(Int_t)(key_trksegm/100);


	   if(m_nsegments_chamber.find(key_chmb) != m_nsegments_chamber.end())
             if(m_nsegments_chamber[key_chmb]==1) {
               Int_t nhit=0;
               for(Int_t k=0;k<6;k++) 
		 if(m_Single_cscSegments_recHitRecordX[key_chmb][k]>-999.0)
                   nhit++;
               if(nhit != (Int_t)nlayers) {
                 //cout<<"Warning - diff. # of hits "<<nhit<<" "<<nlayers<<" "<<key_trksegm<<"  "<<key_chmb<<"  "<<fEvent<<endl;
                 histos->fill1DHist((Float_t)nlayers,"nhits_ne_nlayers","","# of layers given in track segment and different from original segment","Entires",4,8,0.0,8.0,1.0,"Test");
	       }
               if(nhit==(Int_t)nlayers) {
                 Double_t sumx=0.0,sumy=0.0;
                 for(Int_t k=0;k<6;k++) 
		   if(m_Single_cscSegments_recHitRecordX[key_chmb][k]>-999.0) {
                      Int_t key_layer=10*key_chmb+(k+1);
                      if(m_cscSegments_single_trk_recHitRecord.find(key_layer)==m_cscSegments_single_trk_recHitRecord.end()) 
		        m_cscSegments_single_trk_recHitRecord[key_layer]=zero6;
                      m_cscSegments_single_trk_recHitRecord[key_layer][0]=m_Single_cscSegments_recHitRecordX[key_chmb][k];
                      m_cscSegments_single_trk_recHitRecord[key_layer][1]=m_Single_cscSegments_recHitRecordY[key_chmb][k];
                      m_cscSegments_single_trk_recHitRecord[key_layer][2]=-999.0;  
		      m_cscSegments_single_trk_recHitRecord[key_layer][3]=(Double_t) fmuons_pt[i];//Laurent: pt of the associated mu 
		      m_cscSegments_single_trk_recHitRecord[key_layer][4]=(Double_t) fmuons_eta[i];//Laurent: eta of the associated mu 
		      m_cscSegments_single_trk_recHitRecord[key_layer][5]=(Double_t) fmuons_phi[i];//Laurent: eta of the associated mu 
		      //		      cout <<"pt, eta " <<fmuons_pt[i]<<", "<<fmuons_eta[i]<<endl;
                      sumx=sumx+m_Single_cscSegments_recHitRecordX[key_chmb][k];
                      sumy=sumy+m_Single_cscSegments_recHitRecordY[key_chmb][k];
		   }
                 Double_t x_aver=sumx/(Double_t)nhit;
                 Double_t y_aver=sumy/(Double_t)nhit; 

                 if(m_muon_segm.find(key_trksegm)==m_muon_segm.end())
                   m_muon_segm[key_trksegm]=zero3;
	           m_muon_segm[key_trksegm][0]=localX;
                 m_muon_segm[key_trksegm][1]=localY;
                 m_muon_segm[key_trksegm][2]=nlayers;
                 if(nhit==6) {
                   Float_t dx=(Float_t)(x_aver-localX);
                   Float_t dy=(Float_t)(y_aver-localY);
                   histos->fill1DHist(dx,"dx6","","dx, cm","Entires",4,100,-0.5,0.5,1.0,"Test");
                   histos->fill1DHist(dy,"dy6","","dy, cm","Entires",4,100,-0.5,0.5,1.0,"Test");
                   Int_t key_strng=10*station+ring;
                   histos->fill2DHist(dy,((Float_t)m_ordstatring[key_strng]+0.5),"ringstation_vs_dy","","dy, cm","Station/ring, 11,12,13,14,21,22,31,32,41,42","COLZ",100,-0.5,0.5,10,1.0,11.0,1.0,"Test");
                   histos->fill2DHist(dx,((Float_t)m_ordstatring[key_strng]+0.5),"ringstation_vs_dx","","dx, cm","Station/ring, 11,12,13,14,21,22,31,32,41,42","COLZ",100,-0.5,0.5,10,1.0,11.0,1.0,"Test");
                   Int_t statrng=10*station+ring;
                   if(statrng != 11 && statrng != 14) {
                     ss.str("");
                     ss<<"Yloc_vs_dy_ME"<<statrng;
		   if(statrng==12 || statrng==13 || statrng==21 || statrng==22)
                     histos->fill2DHist(dy,y_aver,ss.str().c_str(),"","dy, cm","Yloc, cm","COLZ",25,0.0,0.25,75,-150.0,150.0,1.0,"Test");
	           if(statrng==31 || statrng==32 || statrng==41 || statrng==42)
		     histos->fill2DHist(dy,y_aver,ss.str().c_str(),"","dy, cm","Yloc, cm","COLZ",25,-0.25,0.0,75,-150.0,150.0,1.0,"Test");
		   }
		 } // end of if(nhit==6)
	       } // end of if(nhit==(Int_t)nlayers)
	     } // end of if(m_nsegments_chamber[key_chmb]==1)
	   } // end of if j<10
	 } // end of for(UInt_t j=0;j<(*fmuons_cscSegmentRecord_nRecHits)[i]...
         histos->fill1DHist((Float_t)segmindmx,"segmindmx_per_event","","Max. segment index in nonempty track per event","Entires",4,10,0.0,10.0,1.0,"Test");
       } // end of if (*fmuons_cscSegmentRecord_nRecHits)[i].size() > 0
     } // end of for(UInt_t i=0;i<fmuons_cscSegmentRecord_nRecHits->size();i++)
     histos->fill1DHist((Float_t)trackneindmx,"trackneindmx_per_event","","Max. nonempty track index per event","Entires",4,30,0.0,30.0,1.0,"Test");

     if(m_cscSegments_single_trk_recHitRecord.size() > 0) 
       histos->fill1DHist((Float_t)m_cscSegments_single_trk_recHitRecord.size(),"single_segm_rechits_trk_per_event","","Track single segment hits per event","Entries",4,100,0.0,100.0,1.0,"Test");
     if(m_muon_segm.size() > 0) histos->fill1DHist((Float_t)m_muon_segm.size(),"single_segm_tracks_per_event","","# of single track_segments per event","Entires",4,20,0.0,20.0,1.0,"Test");
     } // end of if single muon track per event (trackne==1)
     } // end of    if(m_Single_cscSegments_recHitRecordX.size() > 0) 
}

/* *******************  GetRecHitsSumQ ********************************* */

void AnalysisGasGain::GetRecHitsSumQ(HistMan* histos) {

     if(m_cscSegments_single_trk_recHitRecord.size() > 0) {
       for(Int_t irechit=0;irechit<frecHits2D_nRecHits2D;irechit++) {
          Int_t ring=frecHits2D_ID_ring[irechit];
          // look at hits with SumQ>0 and not from ME1/4
	  if((frecHits2D_SumQ[irechit] > 0.0) ) { // Commented out Laurent on 27/11/2017
	  //          if((frecHits2D_SumQ[irechit] > 0.0) && (ring !=4)) {
            Int_t endcap=frecHits2D_ID_endcap[irechit];
            Int_t station=frecHits2D_ID_station[irechit];
            Int_t chamber=frecHits2D_ID_chamber[irechit];
            Int_t layer=frecHits2D_ID_layer[irechit];
            Int_t key_layer=100000*endcap+10000*station+1000*ring+
                         10*chamber+layer;
            Double_t xloc=frecHits2D_localX[irechit];
            Double_t yloc=frecHits2D_localY[irechit];
            Double_t sumq=frecHits2D_SumQ[irechit];

            if(m_cscSegments_single_trk_recHitRecord.find(key_layer)!=m_cscSegments_single_trk_recHitRecord.end()) {
              Double_t dx=xloc-m_cscSegments_single_trk_recHitRecord[key_layer][0];
              Double_t dy=yloc-m_cscSegments_single_trk_recHitRecord[key_layer][1];
	      
	      if(fabs(dx) < 0.0001 && fabs(dy) < 0.0001)
               m_cscSegments_single_trk_recHitRecord[key_layer][2]=sumq;

	    } // end of if(m_cscSegments_single_trk_recHitRecord.find...
	  } // end of  if((frecHits2D_SumQ[irechit] > 0.0)
       } // end of  for(Int_t irechit=0;irechit<frecHits2D_nRecHits2D;

        for(map<Int_t, std::vector <Double_t> >::iterator It=m_cscSegments_single_trk_recHitRecord.begin(); It!=m_cscSegments_single_trk_recHitRecord.end(); It++) {
       if((*It).second[2] > 0.0) {
         Int_t key_layer=(*It).first;
     
         if(m_cscSegments_single_trk_recHitRecord_final.find(key_layer)==
	    m_cscSegments_single_trk_recHitRecord_final.end())
           m_cscSegments_single_trk_recHitRecord_final[key_layer]=
	   m_cscSegments_single_trk_recHitRecord[key_layer];
       }
	} // end of  for(map<Int_t, std::vector <Double_t> >::iterator It=m_cscSegments_single_trk_recHitRecord.begin()

        Float_t df=(Float_t)m_cscSegments_single_trk_recHitRecord.size() - 
	           (Float_t)m_cscSegments_single_trk_recHitRecord_final.size();
	      
	//Laurent        histos->fill1DHist(df,"diff_map_sizes","","Difference in two map sizes","Entries",4,10,0.0,10.0,1.0,"Test");
        //if(df !=0.0) 
	  //cout<<"Warning, different sizes "<<m_cscSegments_single_trk_recHitRecord.size()<<" "<<m_cscSegments_single_trk_recHitRecord_final.size()<<" "<<fEvent<<endl;
	// histos->fill1DHist((Float_t)m_cscSegments_single_trk_recHitRecord_final.size(),"final_used_rechits_no_ME14_per_event","","Number of used rechits(no ME14) per event","Entries",4,100,0.0,100.0,1.0,"Test");    //laurent: I commented this line:

     } // end of if(m_cscSegments_single_trk_recHitRecord.size() > 0)
}

/* ********************  AddME14RecHits ******************************* */

void AnalysisGasGain::AddME14RecHits() {

     if(m_RecHitlayerME14_final.size() > 0 )
       for(map<Int_t, std::vector <Double_t> >::iterator It=m_RecHitlayerME14_final.begin(); It!=m_RecHitlayerME14_final.end(); ++It) {
	 //if(m_cscSegments_single_trk_recHitRecord_final.find((*It).first) !=
      //      m_cscSegments_single_trk_recHitRecord_final.end()) 
       //    cout<<"Error, key exists  "<<(*It).first<<endl;
         if(m_cscSegments_single_trk_recHitRecord_final.find((*It).first) ==
            m_cscSegments_single_trk_recHitRecord_final.end()) {

           m_cscSegments_single_trk_recHitRecord_final[(*It).first]=
	     (*It).second;
	 }
       } // end of for(map<Int_t, std::vector <Double_t> >::iterator It=m_RecHitlayerME14_final
}

/* *******************  FillSumQHists ********************************** */

void AnalysisGasGain::FillSumQHists(HistMan* histos) {

ostringstream ss;

       for(map<Int_t, std::vector <Double_t> >::iterator It=m_cscSegments_single_trk_recHitRecord_final.begin(); It!=m_cscSegments_single_trk_recHitRecord_final.end(); ++It) {

          Int_t key_layer=(*It).first;
          Int_t endcap=key_layer/100000;
          Int_t srcl=key_layer-100000*endcap; Int_t station=srcl/10000;
          Int_t rcl=srcl-10000*station;       Int_t ring=rcl/1000;
          Int_t cl=rcl-1000*ring; Int_t chamber=cl/10;
          Int_t layer=cl-10*chamber;

          Int_t key_layer_test=100000*endcap+10000*station+1000*ring+
                                                        10*chamber+layer;
          //if(key_layer!=key_layer_test) cout<<"Error key_layer key_layer_test "<<key_layer<<" "<<key_layer_test<<endl;
          Int_t stationring=10*station+ring;

          // find HV segment
	  Float_t yloc=(Float_t)(*It).second[1];
          Int_t hvsgm=doHVsegment(yloc,station,ring,layer);
	  //        histos->fill1DHist((float)hvsgm,"HV_segment","","HV segment #","Entries",4,6,0.0,6.0,1.0,"Hists"); //commented out by Laurent
          Float_t sumq=(Float_t)(*It).second[2];
     
	  _ptmuon =(Double_t)(*It).second[3];
	  _etamuon =(Double_t)(*It).second[4];
	  _phimuon =(Double_t)(*It).second[5];
	  //	  cout << "eta, pt  " <<_etamuon<<", "<<_ptmuon <<endl;
          if(hvsgm > 0) { // skip rechits having no HV segment
            /* Following commented out by Laurent
            ss.str("");
            ss<<"SumQ_";
            ss<<endcap<<station<<ring;
            if(chamber<10) ss<<0;
            ss<<chamber<<layer;
            if(stationring != 11 && stationring!=14) ss<<hvsgm;


	      histos->fill1DHist(sumq,ss.str().c_str(),ss.str().c_str(),"recHit SumQ","Entries",4,4000,0.0,4000.0,1.0,"HistsSegm"); 
	    //	    here to add q vs lumi
	    //best structure is to have a tree with sumq, lumi, pressure, ..

            ss.str("");
            ss<<"SumQ_";
            ss<<station<<ring;
            histos->fill1DHist(sumq,ss.str().c_str(),ss.str().c_str(),"recHit SumQ","Entries",4,4000,0.0,4000.0,1.0,"Hists");

            histos->fill1DHist(sumq,"SumQ","","recHit SumQ","Entries",4,4000,0.0,4000.0,1.0,"Hists");

            if(stationring == 11 || stationring==14) {
              ss.str(""); ss<<"SumQ_ME11_ME14";
              histos->fill1DHist(sumq,ss.str().c_str(),ss.str().c_str(),"recHit SumQ","Entries",4,4000,0.0,4000.0,1.0,"Hists");
              ss.str(""); ss<<"Yloc_ME11_ME14";
               histos->fill1DHist(yloc,ss.str().c_str(),ss.str().c_str(),"recHitYloc, cm","Entries",4,200,-100.0,100.0,1.0,"Hists");
	    } // end of if(stationring == 11 || stationring==14)
	    */

	    _rhid = 1000000 * endcap + 100000*station + 10000*ring + 100*chamber + 10*layer  + hvsgm ;
	    _stationring = station * 10+ ring;
	    _runNb = fRun ;
	    _lumiBlock =fLumiSect ;
	    _bunchcrossing = fBunchCrossing;
	    _eventNb = fEvent;
	    _timesecond =ftimeSecond ;
	    /*	    cout <<"vt "<< (int)fvertex_nVertex <<
	      ", "<<  (unsigned int)fvertex_nVertex<<
	      ", "<<  (float)fvertex_nVertex<<
	      ", "<<  (double)fvertex_nVertex<< 
	      ", "<<  (unsigned long)fvertex_nVertex<<
	      ", "<<  (long)fvertex_nVertex<<
	      endl;// ", "<<_n_PV <<endl;*/
	    //_n_PV = fvertex_nVertex;

	    _rhsumQ_RAW = sumq;
	    std::pair<double,double>  gasgainandhv = UncorrGasGain_HVInitial2016(sumq,fRun,_stationring,_rhid);
	    //	    cout << "run, sumq, stationring, rhid: " << fRun <<", "<<sumq<<", "<<_stationring<<", "<<_rhid <<endl;
	    _rhsumQ =  gasgainandhv.first;
	    _HV =  gasgainandhv.second;

	    int iregion = GetRegionIdx(station,ring,hvsgm);
	    if(iregion >=0)  outputtree[iregion]->Fill();
	    //else cout <<"region not found! " <<endl;
	    

	  } // end if (hvsgm > 0)
       } // end of   for(map<Int_t, std::vector <Double_t> >::iterator It=m_cscSegments_single_trk_recHitRecord_final.begin()

}

/* ********************  CycleTree ************************************* */

void AnalysisGasGain::CycleTree(HistMan* histos) {

  m_RunEvent.clear();
  m_Run_usedevents.clear();
  m_Run_usedhits.clear();
  m_RunStart.clear();
  m_RunEnd.clear();

  TFile *histrootfile = new TFile(histrootname.c_str(), "RECREATE");
  TFile *f =  TFile::Open(ntuplename.c_str());

  TTree *tree = (TTree*)f->Get("cscRootMaker/Events");
  nentries = tree->GetEntries();
  //cout<<"Total entries       "<<nentries<<endl;
  if(flag_stat>0) nentries=flag_stat;
  //cout<<"Entries to read in  "<<nentries<<endl;
  //cout<<endl;

  // Get branches
  TBranch *b_Run=tree->GetBranch("Run");
  TBranch *b_LumiSect=tree->GetBranch("LumiSect");
  //TBranch *b_vertex_nVertex=tree->GetBranch("vertex_nVertex");
  TBranch *b_Event=tree->GetBranch("Event");
  TBranch *b_timeSecond=tree->GetBranch("timeSecond");
  TBranch *b_BunchCrossing=tree->GetBranch("BunchCrossing");

  TBranch *b_recHits2D_nRecHits2D=tree->GetBranch("recHits2D_nRecHits2D");
  TBranch *b_recHits2D_ID_endcap=tree->GetBranch("recHits2D_ID_endcap");
  TBranch *b_recHits2D_ID_station=tree->GetBranch("recHits2D_ID_station");
  TBranch *b_recHits2D_ID_ring=tree->GetBranch("recHits2D_ID_ring");
  TBranch *b_recHits2D_ID_chamber=tree->GetBranch("recHits2D_ID_chamber");
  TBranch *b_recHits2D_ID_layer=tree->GetBranch("recHits2D_ID_layer");
  TBranch *b_recHits2D_localX=tree->GetBranch("recHits2D_localX");
  TBranch *b_recHits2D_localY=tree->GetBranch("recHits2D_localY");
  TBranch *b_recHits2D_SumQ=tree->GetBranch("recHits2D_SumQ");
  
  TBranch *b_cscSegments_recHitRecord_endcap=tree->GetBranch("cscSegments_recHitRecord_endcap");
  TBranch *b_cscSegments_recHitRecord_station=tree->GetBranch("cscSegments_recHitRecord_station");
  TBranch *b_cscSegments_recHitRecord_ring=tree->GetBranch("cscSegments_recHitRecord_ring");
  TBranch *b_cscSegments_recHitRecord_chamber=tree->GetBranch("cscSegments_recHitRecord_chamber");
  TBranch *b_cscSegments_recHitRecord_layer=tree->GetBranch("cscSegments_recHitRecord_layer");
  TBranch *b_cscSegments_recHitRecord_localX=tree->GetBranch("cscSegments_recHitRecord_localX");
  TBranch *b_cscSegments_recHitRecord_localY=tree->GetBranch("cscSegments_recHitRecord_localY");

  TBranch *b_muons_cscSegmentRecord_nRecHits=tree->GetBranch("muons_cscSegmentRecord_nRecHits");
  TBranch *b_muons_cscSegmentRecord_endcap=tree->GetBranch("muons_cscSegmentRecord_endcap");
  TBranch *b_muons_cscSegmentRecord_station=tree->GetBranch("muons_cscSegmentRecord_station");
  TBranch *b_muons_cscSegmentRecord_ring=tree->GetBranch("muons_cscSegmentRecord_ring");
  TBranch *b_muons_cscSegmentRecord_chamber=tree->GetBranch("muons_cscSegmentRecord_chamber");
  TBranch *b_muons_cscSegmentRecord_localX=tree->GetBranch("muons_cscSegmentRecord_localX");
  TBranch *b_muons_cscSegmentRecord_localY=tree->GetBranch("muons_cscSegmentRecord_localY");

  TBranch *b_muons_nMuons=tree->GetBranch("muons_nMuons");
  TBranch *b_muons_pt=tree->GetBranch("muons_pt");
  TBranch *b_muons_eta=tree->GetBranch("muons_eta");
  TBranch *b_muons_phi=tree->GetBranch("muons_phi");
  TBranch *b_muons_dz=tree->GetBranch("muons_dz");
  TBranch *b_muons_dxy=tree->GetBranch("muons_dxy");
  TBranch *b_muons_isoCH03=tree->GetBranch("muons_isoCH03");

  // Set addresses
  b_Run->SetAddress(&fRun);
  b_Event->SetAddress(&fEvent);
  b_LumiSect->SetAddress(&fLumiSect);
  b_timeSecond->SetAddress(&ftimeSecond);
  // b_vertex_nVertex->SetAddress(&fvertex_nVertex);
  
  b_recHits2D_nRecHits2D->SetAddress(&frecHits2D_nRecHits2D);
  b_recHits2D_ID_endcap->SetAddress(frecHits2D_ID_endcap); // no & for array
  b_recHits2D_ID_station->SetAddress(frecHits2D_ID_station);
  b_recHits2D_ID_ring->SetAddress(frecHits2D_ID_ring);
  b_recHits2D_ID_chamber->SetAddress(frecHits2D_ID_chamber);
  b_recHits2D_ID_layer->SetAddress(frecHits2D_ID_layer);
  b_recHits2D_localX->SetAddress(frecHits2D_localX);
  b_recHits2D_localY->SetAddress(frecHits2D_localY);
  b_recHits2D_SumQ->SetAddress(frecHits2D_SumQ); 

  b_cscSegments_recHitRecord_endcap->SetAddress(&fcscSegments_recHitRecord_endcap);
  b_cscSegments_recHitRecord_station->SetAddress(&fcscSegments_recHitRecord_station);
  b_cscSegments_recHitRecord_ring->SetAddress(&fcscSegments_recHitRecord_ring);
  b_cscSegments_recHitRecord_chamber->SetAddress(&fcscSegments_recHitRecord_chamber);
  b_cscSegments_recHitRecord_layer->SetAddress(&fcscSegments_recHitRecord_layer);
  b_cscSegments_recHitRecord_localX->SetAddress(&fcscSegments_recHitRecord_localX);
  b_cscSegments_recHitRecord_localY->SetAddress(&fcscSegments_recHitRecord_localY);

  b_muons_cscSegmentRecord_nRecHits->SetAddress(&fmuons_cscSegmentRecord_nRecHits);
  b_muons_cscSegmentRecord_endcap->SetAddress(&fmuons_cscSegmentRecord_endcap);
  b_muons_cscSegmentRecord_station->SetAddress(&fmuons_cscSegmentRecord_station);
  b_muons_cscSegmentRecord_ring->SetAddress(&fmuons_cscSegmentRecord_ring);
  b_muons_cscSegmentRecord_chamber->SetAddress(&fmuons_cscSegmentRecord_chamber);
  b_muons_cscSegmentRecord_localX->SetAddress(&fmuons_cscSegmentRecord_localX);
  b_muons_cscSegmentRecord_localY->SetAddress(&fmuons_cscSegmentRecord_localY);

  b_muons_nMuons->SetAddress(&fmuons_nMuons);
  b_muons_pt->SetAddress(fmuons_pt);
  b_muons_eta->SetAddress(fmuons_eta);
  b_muons_phi->SetAddress(fmuons_phi);
  b_muons_dz->SetAddress(fmuons_dz);
  b_muons_dxy->SetAddress(fmuons_dxy);
  b_muons_isoCH03->SetAddress(fmuons_isoCH03);
  fcscSegments_recHitRecord_endcap  = 0; 
  fcscSegments_recHitRecord_station = 0; 
  fcscSegments_recHitRecord_ring    = 0;  
  fcscSegments_recHitRecord_chamber = 0; 
  fcscSegments_recHitRecord_layer   = 0; 
  fcscSegments_recHitRecord_localX  = 0; 
  fcscSegments_recHitRecord_localY  = 0;

  fmuons_cscSegmentRecord_nRecHits  = 0;
  fmuons_cscSegmentRecord_endcap    = 0;
  fmuons_cscSegmentRecord_station   = 0;
  fmuons_cscSegmentRecord_ring      = 0;
  fmuons_cscSegmentRecord_chamber   = 0;
  fmuons_cscSegmentRecord_localY    = 0;
  fmuons_cscSegmentRecord_localX    = 0;


  // *********************************************
  // ***  Cycling over tree
  // *********************************************


  ULong64_t runnb_previous_event(0),  lumis_previous_event(0);


  for(Int_t ient=0;ient<nentries;ient++) {

     b_Run->GetEntry(ient);
     b_Event->GetEntry(ient);
     b_LumiSect->GetEntry(ient);
     b_timeSecond->GetEntry(ient);
     
     //b_vertex_nVertex->GetEntry(ient);
     b_BunchCrossing->GetEntry(ient);

     
     b_recHits2D_nRecHits2D->GetEntry(ient);
     b_recHits2D_ID_endcap->GetEntry(ient);
     b_recHits2D_ID_station->GetEntry(ient);
     b_recHits2D_ID_ring->GetEntry(ient);
     b_recHits2D_ID_chamber->GetEntry(ient);
     b_recHits2D_ID_layer->GetEntry(ient);
     b_recHits2D_localX->GetEntry(ient);
     b_recHits2D_localY->GetEntry(ient);
     b_recHits2D_SumQ->GetEntry(ient);
     
     b_cscSegments_recHitRecord_endcap->GetEntry(ient);
     b_cscSegments_recHitRecord_station->GetEntry(ient);
     b_cscSegments_recHitRecord_ring->GetEntry(ient);
     b_cscSegments_recHitRecord_chamber->GetEntry(ient);
     b_cscSegments_recHitRecord_layer->GetEntry(ient);
     b_cscSegments_recHitRecord_localX->GetEntry(ient);
     b_cscSegments_recHitRecord_localY->GetEntry(ient);

     b_muons_cscSegmentRecord_nRecHits->GetEntry(ient);
     b_muons_cscSegmentRecord_endcap->GetEntry(ient);
     b_muons_cscSegmentRecord_station->GetEntry(ient);
     b_muons_cscSegmentRecord_ring->GetEntry(ient);
     b_muons_cscSegmentRecord_chamber->GetEntry(ient);
     b_muons_cscSegmentRecord_localX->GetEntry(ient);
     b_muons_cscSegmentRecord_localY->GetEntry(ient);

     b_muons_pt->GetEntry(ient);
     b_muons_eta->GetEntry(ient);
     b_muons_phi->GetEntry(ient);
     b_muons_dz->GetEntry(ient);
     b_muons_dxy->GetEntry(ient);
     b_muons_isoCH03->GetEntry(ient);

     m_nRecHitlayer.clear();
     m_nRecHitchamber.clear();
     m_nRecHitlayerME14.clear();
     m_RecHitlayerME14_final.clear();
     m_cscSegments_recHitRecordX.clear();
     m_cscSegments_recHitRecordY.clear();
     m_nsegments_chamber.clear();
     m_muon_segm.clear();
     m_Single_cscSegments_recHitRecordX.clear();
     m_Single_cscSegments_recHitRecordY.clear();
     m_cscSegments_single_trk_recHitRecord.clear();
     m_cscSegments_single_trk_recHitRecord_final.clear();

     _pressure = getpressure(ftimeSecond);
     _temperature =0;
     



     for( int iM = 0; iM< fmuons_nMuons;iM++) {fmuons_Zcand[iM] = false; fmuons_isomuondzdxy[iM] = false;}
     //Skim: 2 muons pt 10, 70<M(mumu)<110
     passZmumusel= false;
     bool passisomuondzdxy = false;
     double mass =-1;
     for( int iM = 0; iM<  fmuons_nMuons;iM++){

       if(  fmuons_pt[iM]<10) continue;
       if(fabs(fmuons_dz[iM]) >0.2) continue;
       if(fabs(fmuons_dxy[iM]) >0.2) continue;
       if(fabs(fmuons_isoCH03[iM]) >2) continue;
       fmuons_isomuondzdxy[iM]=true;
       passisomuondzdxy =true;
       TLorentzVector mu1; 
       for( int jM= iM+1; jM<  fmuons_nMuons ;jM++){
	 if(  fmuons_pt[jM]<10) continue;
	 if(fabs(fmuons_dz[jM]) >0.2) continue;
	 if(fabs(fmuons_dxy[jM]) >0.2) continue;
	 if(fabs(fmuons_isoCH03[jM]) >2) continue;
	 
	 TLorentzVector mu2;
	 mu1.SetPtEtaPhiM( fmuons_pt[iM], fmuons_eta[iM], fmuons_phi[iM],0);
	 mu2.SetPtEtaPhiM( fmuons_pt[jM], fmuons_eta[jM], fmuons_phi[jM],0);
	 mass = (mu1+mu2).Mag();
	 
	 if(mass>70&&mass<110){ 
	   passZmumusel= true;
	   fmuons_Zcand[iM]=true; 
	   fmuons_Zcand[jM]=true; 
	 }
       }
     }

     if(!passZmumusel&& !passisomuondzdxy) continue;
     if(runnb_previous_event != fRun ||   lumis_previous_event !=  fLumiSect)   _instlumi =instlumi(fRun, fLumiSect) ;
     
     if(runnb_previous_event != fRun ) _integratelumi = integlumi2016(fRun);
     
     
     runnb_previous_event =fRun; 
     lumis_previous_event =  fLumiSect ;
     

     // get Run, Event, Start, End
     Int_t key_run=(Int_t)fRun;

     if(m_RunEvent.find(key_run) == m_RunEvent.end()) {
       m_RunEvent[key_run]=0;
       m_Run_usedevents[key_run]=0;
       m_Run_usedhits[key_run]=0;
       // get max number, it should be 4294967295 for unsigned int
       m_RunStart[key_run]=std::numeric_limits<unsigned int>::max();       
       m_RunEnd[key_run]=0;
     }
     m_RunEvent[key_run]=m_RunEvent[key_run]+1;
     if(ftimeSecond>m_RunEnd[key_run]) m_RunEnd[key_run]=ftimeSecond;
     if(ftimeSecond<m_RunStart[key_run]) m_RunStart[key_run]=ftimeSecond;

     //************************************************************************
     // Check the presence of needed and not empty vectors
     //************************************************************************

     Int_t recsegtrk=0;
     if(frecHits2D_nRecHits2D > 0) recsegtrk=recsegtrk+1;
     if(fcscSegments_recHitRecord_endcap->size() > 0) recsegtrk=recsegtrk+2;
     if(fmuons_cscSegmentRecord_nRecHits->size() > 0) {
       Int_t ncscsegm=0;
       for(UInt_t i=0;i<fmuons_cscSegmentRecord_nRecHits->size();i++) 
	 if((*fmuons_cscSegmentRecord_nRecHits)[i].size() > 0) ncscsegm++; 
       if(ncscsegm > 0) recsegtrk=recsegtrk+4;
     }
     histos->fill1DHist((Float_t)recsegtrk,"recsegtrk","","Bit 1-RecHits2D, Bit 2-Segments and Bit 3-Tracks per event","Entries",4,8,0.0,8.0,1.0,"Test");
  
     if(recsegtrk==7) { // Analyse event only when all 3 vectors not empty //Laurent: this ensures there's at least 1 rechit, 1 segment and 1 muon associated to them (??)
      //if(ient<flag_print) cout<<endl<<"*** "<<ient+1<< " Event "<<fEvent<<endl;


     //*****************************************************************
     //  Treat ME1/4 differently (due 3 strips ganging),
     //  using only frecHits2D_nRecHits2D;
     //  fill maps m_nRecHitlayer,m_nRecHitchamber (# of hits per layer
     //  and chamber)
     //******************************************************************

      //     GetME14RecHits(histos);//Commented out  by laurent: now treating ME1/4 (a.k.a ME11a) as other station/rings

     //************************************************************************
     // Cycling thru segments in fcscSegments_recHitRecord_*, 
     // put their rechits X,Y local into 
     // maps m_cscSegments_recHitRecordX,*Y[key_segment][0-5], 0-5 are layers
     // and count # of segments per chamber in m_nsegments_chamber[chamber]
     //************************************************************************

     GetSegments(histos);

     //*******************************************************************
     // Cycling thru tracks in event and segments in them, put to map  
     // m_cscSegments_single_trk_recHitRecord[key_layer][0-2]
     //corresponding rechits
     //*******************************************************************

     GetTracks(histos);

     //**************************************
     //*** cycling over recHits2D_nRecHits to find SumQ and put it into
     //*** map m_cscSegments_single_trk_recHitRecord[key_layer][0-2]
     //***************************************

     GetRecHitsSumQ(histos);

     //**********************************************************************
     // Add m_RecHitlayerME14_final to map 
     // m_cscSegments_single_trk_recHitRecord_final
     //**********************************************************************

     //     AddME14RecHits(); Commented out Laurent

      if(m_cscSegments_single_trk_recHitRecord_final.size() > 0) {
        histos->fill1DHist((Float_t)m_cscSegments_single_trk_recHitRecord_final.size(),"final_used_rechits_per_event","","Number of used rechits per event","Entries",4,100,0.0,100.0,1.0,"Test");
         m_Run_usedevents[key_run]=m_Run_usedevents[key_run]+1;
         m_Run_usedhits[key_run]=m_Run_usedhits[key_run]+(Int_t)m_cscSegments_single_trk_recHitRecord_final.size();
      }

     //**********************************************************************
     // Cycling thru  m_cscSegments_single_trk_recHitRecord_final to SumQ
     // histograms in HV segments
     //**********************************************************************

     if(m_cscSegments_single_trk_recHitRecord_final.size() > 0) 
        FillSumQHists(histos); 


     } // end of if(recsegtrk==7)
  } // end of  for(Int_t ient=0;

  tree->ResetBranchAddresses();

  //************************************************************************
  // End of tree analysis printout
  //**************************************************************************

  //cout<<endl;
  Int_t cnt=0,cnt_readin=0,cnt_used=0,cnt_usedhits=0;
  for(std::map<Int_t,Int_t>::iterator It=m_RunEvent.begin(); It!= m_RunEvent.end();++It) {
     Int_t key=(*It).first;
     cnt++;     
     Int_t dur=(Int_t)(m_RunEnd[key]-m_RunStart[key]);
     cnt_readin=cnt_readin+m_RunEvent[key];
     cnt_used=cnt_used+m_Run_usedevents[key];
     cnt_usedhits=cnt_usedhits+m_Run_usedhits[key];
     //cout<<cnt<<" Run  Events  Start  End  Duration  Used events  Used hits "<<key<<" "<<(*It).second<<" "<<m_RunStart[key]<<" "<<m_RunEnd[key]<<" "<<dur<<" "<<m_Run_usedevents[key]<<" "<<m_Run_usedhits[key]<<endl;
       }
  //cout<<"--------------------------------------------------"<<endl;
  //cout<<"Total used hits "<<cnt_usedhits<<" in "<<cnt_used<<" used events  from "<<cnt_readin<<" read in events in "<<m_RunEvent.size()<<" runs"<<endl;
  //cout<<endl;
  //cout<<" End of AnalysisGasGain::CycleTree "<<endl;

  //*************************************************************************
  // write and close output file with hists always first in case if hists
  // were stored in f directory
  //************************************************************************

  histos->writeHists(histrootfile);
  histrootfile->Close();
  f->Close();
}


