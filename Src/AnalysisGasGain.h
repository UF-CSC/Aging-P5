#ifndef ROOT_AnalysisGasGain
#define ROOT_AnalysisGasGain

#include "HistMan.h"
#include "TTree.h"

class AnalysisGasGain : public TObject {

private:

  string  ntuplename;      // input ntuple file
  string  histrootname;    // output ROOT file with hists

  Int_t nentries;          // Tree entries
  Int_t entries_analyzed;  // # of analyzed entries

  Int_t flag_stat;         // 0 - use all entries,>0 - use flag_stat statistics
  Int_t flag_print;        // 0-do not print debug info, >0 - print it

  std::vector<Double_t> zero3,zero6,zero5;
  
  // Variables for tree


  ULong64_t   fEvent,fRun, fLumiSect;
  UInt_t      ftimeSecond;
  Int_t fvertex_nVertex;
  Int_t  fBunchCrossing;
  
  Int_t       frecHits2D_nRecHits2D;
  Int_t       frecHits2D_ID_endcap[10000], frecHits2D_ID_station[10000],
              frecHits2D_ID_ring[10000],   frecHits2D_ID_chamber[10000], 
              frecHits2D_ID_layer[10000];
  Double_t    frecHits2D_localX[10000],  frecHits2D_localY[10000],    
              frecHits2D_SumQ[10000];

  vector<vector<Double_t> > *fcscSegments_recHitRecord_endcap;
  vector<vector<Double_t> > *fcscSegments_recHitRecord_ring;
  vector<vector<Double_t> > *fcscSegments_recHitRecord_station;
  vector<vector<Double_t> > *fcscSegments_recHitRecord_chamber;
  vector<vector<Double_t> > *fcscSegments_recHitRecord_layer;
  vector<vector<Double_t> > *fcscSegments_recHitRecord_localX;
  vector<vector<Double_t> > *fcscSegments_recHitRecord_localY;

  std::vector< std::vector<Double_t> > *fmuons_cscSegmentRecord_nRecHits;
  std::vector< std::vector<Double_t> > *fmuons_cscSegmentRecord_endcap;
  std::vector< std::vector<Double_t> > *fmuons_cscSegmentRecord_station;
  std::vector< std::vector<Double_t> > *fmuons_cscSegmentRecord_ring;
  std::vector< std::vector<Double_t> > *fmuons_cscSegmentRecord_chamber;
  std::vector< std::vector<Double_t> > *fmuons_cscSegmentRecord_localY;
  std::vector< std::vector<Double_t> > *fmuons_cscSegmentRecord_localX;

  Int_t fmuons_nMuons;  
  Double_t fmuons_pt[100] ; 
  Double_t fmuons_eta[100] ; 
  Double_t fmuons_phi[100] ; 

  Double_t fmuons_dz[100] ; 
  Double_t fmuons_dxy[100] ; 
  Double_t fmuons_isoCH03[100] ; 
  Bool_t fmuons_Zcand[100];
  Bool_t fmuons_isomuondzdxy[100];

  // Yloc boundaries of HV segments in CSC layers
  // Low and High Y local coordinates (cm) of the segments
  Float_t  me12YlocHVsgmLow[3],   me12YlocHVsgmHigh[3],
           me13YlocHVsgmLow[3],   me13YlocHVsgmHigh[3], 
           me21YlocHVsgmLow[3],   me21YlocHVsgmHigh[3], 
           me31YlocHVsgmLow[3],   me31YlocHVsgmHigh[3],
           me41YlocHVsgmLow[3],   me41YlocHVsgmHigh[3],
           me234_2YlocHVsgmLow[5],me234_2YlocHVsgmHigh[5];
  TFile * myoutfilefortree[32] ;
  TTree * outputtree[32]; //output tree 
  //Format is the following: 
  //treeME11a
  //treeME11b
  //treeME12HV1
  //treeME12HV2
  //treeME12HV3
  //treeME13HV1
  //treeME13HV2
  //treeME13HV3
  //treeME21HV1
  //treeME21HV2
  //treeME21HV3
  //treeME31HV1
  //treeME31HV2
  //treeME31HV3
  //treeME41HV1
  //treeME41HV2
  //treeME41HV3
  //treeME22HV1
  //treeME22HV2
  //treeME22HV3
  //treeME22HV4
  //treeME22HV5
  //treeME32HV1
  //treeME32HV2
  //treeME32HV3
  //treeME32HV4
  //treeME32HV5
  //treeME42HV1
  //treeME42HV2
  //treeME42HV3
  //treeME42HV4
  //treeME42HV5
  ULong64_t _eventNb,_runNb,_lumiBlock;
  int _rhid, _stationring;
  double _rhsumQ;
  double _rhsumQ_RAW;
  double _HV;
  double _pressure;
  double _temperature;
  double _instlumi;
  double _integratelumi;
  UInt_t _timesecond ;
  Int_t _n_PV;
  Int_t _bunchcrossing;
  Bool_t passZmumusel;
  double _ptmuon;
  double _etamuon;
  double _phimuon;

public:

  AnalysisGasGain();
  virtual ~AnalysisGasGain();

  void Setup(Int_t,Int_t);
  
  void SetupTree(string,string);

  void SetupPrint();

  Int_t doHVsegment(Float_t, Int_t, Int_t, Int_t);

  void Analyze(HistMan*);
  void GetME14RecHits(HistMan*);
  void GetSegments(HistMan*);
  void GetTracks(HistMan*);
  void GetRecHitsSumQ(HistMan*);
  void FillSumQHists(HistMan*);
  void AddME14RecHits();
  void CycleTree(HistMan*);
  TString GetRegionName( int i){
    if(i==0)return "ME11a";
    if(i==1)return "ME11b";
    if(i==2)return "ME12HV1";
    if(i==3)return "ME12HV2";
    if(i==4)return "ME12HV3";
    if(i==5)return "ME13HV1";
    if(i==6)return "ME13HV2";
    if(i==7)return "ME13HV3";
    if(i==8)return "ME21HV1";
    if(i==9)return "ME21HV2";
    if(i==10)return "ME21HV3";
    if(i==11)return "ME31HV1";
    if(i==12)return "ME31HV2";
    if(i==13)return "ME31HV3";
    if(i==14)return "ME41HV1";
    if(i==15)return "ME41HV2";
    if(i==16)return "ME41HV3";
    if(i==17)return "ME22HV1";
    if(i==18)return "ME22HV2";
    if(i==19)return "ME22HV3";
    if(i==20)return "ME22HV4";
    if(i==21)return "ME22HV5";
    if(i==22)return "ME32HV1";
    if(i==23)return "ME32HV2";
    if(i==24)return "ME32HV3";
    if(i==25)return "ME32HV4";
    if(i==26)return "ME32HV5";
    if(i==27)return "ME42HV1";
    if(i==28)return "ME42HV2";
    if(i==29)return "ME42HV3";
    if(i==30)return "ME42HV4";
    if(i==31)return "ME42HV5";
    return "";
  };
  int GetRegionIdx(Int_t station, Int_t ring, Int_t hvsegm){
    if(station == 1 && ring ==4) return 0; //ME11a is ME14 ! 
    if(station == 1 && ring ==1) return 1; //ME11b is ME11...


    if(station == 1 && ring ==2 &&hvsegm ==1) return 2;
    if(station == 1 && ring ==2 &&hvsegm ==2) return 3;
    if(station == 1 && ring ==2 &&hvsegm ==3) return 4;

    if(station == 1 && ring ==3 &&hvsegm ==1) return 5;
    if(station == 1 && ring ==3 &&hvsegm ==2) return 6;
    if(station == 1 && ring ==3 &&hvsegm ==3) return 7;

    if(station == 2 && ring ==1 &&hvsegm ==1) return 8;
    if(station == 2 && ring ==1 &&hvsegm ==2) return 9;
    if(station == 2 && ring ==1 &&hvsegm ==3) return 10;

    if(station == 3 && ring ==1 &&hvsegm ==1) return 11;
    if(station == 3 && ring ==1 &&hvsegm ==2) return 12;
    if(station == 3 && ring ==1 &&hvsegm ==3) return 13;

    if(station == 4 && ring ==1 &&hvsegm ==1) return 14;
    if(station == 4 && ring ==1 &&hvsegm ==2) return 15;
    if(station == 4 && ring ==1 &&hvsegm ==3) return 16;


    if(station == 2 && ring ==2 &&hvsegm ==1) return 17;
    if(station == 2 && ring ==2 &&hvsegm ==2) return 18;
    if(station == 2 && ring ==2 &&hvsegm ==3) return 19;
    if(station == 2 && ring ==2 &&hvsegm ==4) return 20;
    if(station == 2 && ring ==2 &&hvsegm ==5) return 21;

    if(station == 3 && ring ==2 &&hvsegm ==1) return 22;
    if(station == 3 && ring ==2 &&hvsegm ==2) return 23;
    if(station == 3 && ring ==2 &&hvsegm ==3) return 24;
    if(station == 3 && ring ==2 &&hvsegm ==4) return 25;
    if(station == 3 && ring ==2 &&hvsegm ==5) return 26;


    if(station == 4 && ring ==2 &&hvsegm ==1) return 27;
    if(station == 4 && ring ==2 &&hvsegm ==2) return 28;
    if(station == 4 && ring ==2 &&hvsegm ==3) return 29;
    if(station == 4 && ring ==2 &&hvsegm ==4) return 30;
    if(station == 4 && ring ==2 &&hvsegm ==5) return 31;

    return -1;
  };

ClassDef(AnalysisGasGain,1) 
};

#endif
