#include "TFile.h"
#include "TTree.h"
#include "TNtuple.h"
#include "TF1.h"
#include "TH1.h"
#include "TH2.h"
#include "TString.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

#include "DataFormats/HeavyIonEvent/interface/CentralityBins.h"

using namespace std;

bool descend(float i,float j) { return (i>j); }

void makeDataCentralityTable(int nbins = 200, const string label = "HFtowers", const char * tag = "CentralityTable_HFtowers_Glauber2015A_eff99_v750x01_mc", double EFF = 0.99){

  TH1D::SetDefaultSumw2();

  //This macro assumes all inefficiency is in the most peripheral bins
  double MXS = 1. - EFF;

  TString inFileName = "/afs/cern.ch/user/a/azsigmon/workspace/CentralityTools/eventtree_MB_data_filtered_750_d20150728.root";
  TFile *inFile = TFile::Open(inFileName);
  TTree *t = (TTree*)inFile->Get("hiEvtAnalyzer/HiTree");

  TFile *outFile = new TFile("CentralityTable_HFtowers200_Glauber2015A_d20150804_v1.root","recreate");

  TDirectory *dir = outFile->mkdir(tag);
  dir->cd();
  TNtuple * nt = new TNtuple("nt","","value:bin:b:npart:ncoll:nhard");

  const int runNum = 1;
  CentralityBins * bins = new CentralityBins(Form("run%d",runNum), tag, nbins);
  bins->table_.reserve(nbins);

  //Here we need a default Glauber for 5 TeV
  TFile * inputMCfile = TFile::Open("/afs/cern.ch/user/a/azsigmon/workspace/CentralityTools/d20150519/CentralityTable_HFtowers_HydjetDrum5_d20150519_v1.root");
  CentralityBins* inputMCtable = (CentralityBins*)inputMCfile->Get("CentralityTable_HFtowers_HydjetDrum5_v740x01_mc/run1");

  ofstream txtfile("output_d20150804.txt");
  txtfile << "Input tree: " << inFileName << endl;

  double binboundaries[nbins+1];
  vector<float> values;

  float hf, hfplus, hfpluseta4, hfminuseta4, hfminus, hfhit, ee, eb, zdc, zdcplus, zdcminus;
  int run, lumi, npix, npixtrks, ntrks;
  t->SetBranchAddress("run",	&run);
  t->SetBranchAddress("lumi",	&lumi);
  t->SetBranchAddress("hiHF",		&hf);
  t->SetBranchAddress("hiHFplus",	&hfplus);
  t->SetBranchAddress("hiHFplusEta4",	&hfpluseta4);
  t->SetBranchAddress("hiHFminus",	&hfminus);
  t->SetBranchAddress("hiHFminusEta4",	&hfminuseta4);
  t->SetBranchAddress("hiHFhit",	&hfhit);
  t->SetBranchAddress("hiZDC",		&zdc);
  t->SetBranchAddress("hiZDCplus",	&zdcplus);
  t->SetBranchAddress("hiZDCminus",	&zdcminus);
  t->SetBranchAddress("hiEE",		&ee);
  t->SetBranchAddress("hiEB",		&eb);
  t->SetBranchAddress("hiNpix",		&npix);
  t->SetBranchAddress("hiNpixelTracks",	&npixtrks);
  t->SetBranchAddress("hiNtracks",	&ntrks);

  bool binHF = label.compare("HFtowers") == 0;
  bool binHFplus = label.compare("HFtowersPlus") == 0;
  bool binHFminus = label.compare("HFtowersMinus") == 0;
  bool binHFplusTrunc = label.compare("HFtowersPlusTrunc") == 0;
  bool binHFminusTrunc = label.compare("HFtowersMinusTrunc") == 0;
  bool binNpix = label.compare("PixelHits") == 0;
  bool binNpixTrks = label.compare("PixelTracks") == 0;
  bool binNtrks = label.compare("Tracks") == 0;

  unsigned int Nevents = t->GetEntries();
  txtfile << "Number of events = " << Nevents << endl << endl;

  for(unsigned int iev = 0; iev < Nevents; iev++) {

    if(iev%50000 == 0) cout<<"Processing event: " << iev << endl;
    t->GetEntry(iev);

    float parameter = -1;
    if(binHF) parameter = hf;
    if(binHFplus) parameter = hfplus;
    if(binHFminus) parameter = hfminus;
    if(binHFplusTrunc) parameter = hfpluseta4;
    if(binHFminusTrunc) parameter = hfminuseta4;
    if(binNpix) parameter = npix;
    if(binNpixTrks) parameter = npixtrks;
    if(binNtrks) parameter = ntrks;

    values.push_back(parameter);

  }

  sort(values.begin(),values.end());

  txtfile << "-------------------------------------" << endl;
  txtfile << label.data() << " based cuts are: " << endl;
  txtfile << "(";

  int size = values.size();
  binboundaries[nbins] = values[size-1];

  for(int i = 0; i < nbins; i++) {
    int entry = (int)( i*(size/EFF/nbins) - size*(1 - EFF)/EFF );
    if(entry < 0 || i == 0) binboundaries[i] = 0;
    else binboundaries[i] = values[entry];
    if(binboundaries[i] < 0) { binboundaries[i] = 0; cout << "*"; }
  }

  for(int i = 0; i < nbins; i++) {
    if(binboundaries[i] < 0) binboundaries[i] = 0;
    txtfile << binboundaries[i] << ", ";
  }
  txtfile << binboundaries[nbins] << ")" << endl << "-------------------------------------" << endl;

  txtfile<<"-------------------------------------"<<endl;
  txtfile<<"# Bin NpartMean NpartSigma NcollMean NcollSigma bMean bSigma BinEdge"<<endl;
  for(int i = 0; i < nbins; i++){
    int ii = nbins-i;
    bins->table_[i].n_part_mean = inputMCtable->NpartMeanOfBin(i);
    bins->table_[i].n_part_var = inputMCtable->NpartSigmaOfBin(i);
    bins->table_[i].n_coll_mean = inputMCtable->NcollMeanOfBin(i);
    bins->table_[i].n_coll_var = inputMCtable->NcollSigmaOfBin(i);
    bins->table_[i].b_mean = inputMCtable->bMeanOfBin(i);
    bins->table_[i].b_var = inputMCtable->bSigmaOfBin(i);
    bins->table_[i].n_hard_mean = inputMCtable->NhardMeanOfBin(i);
    bins->table_[i].n_hard_var = inputMCtable->NhardSigmaOfBin(i);
    bins->table_[i].ecc2_mean  = inputMCtable->eccentricityMeanOfBin(i);
    bins->table_[i].ecc2_var = inputMCtable->eccentricitySigmaOfBin(i);
    bins->table_[i].bin_edge = binboundaries[ii-1];

    txtfile << i << " " << bins->table_[i].n_part_mean << " " << bins->table_[i].n_part_var << " " << bins->table_[i].n_coll_mean << " " << bins->table_[i].n_coll_var << " " <<bins->table_[i].b_mean << " " << bins->table_[i].b_var << " " << bins->table_[i].n_hard_mean << " " << bins->table_[i].n_hard_var << " " << bins->table_[i].bin_edge << " " << endl;
  }
  txtfile<<"-------------------------------------"<<endl;

  outFile->cd();
  dir->cd();
  bins->Write();
  nt->Write();  
  bins->Delete();
  outFile->Write();
  txtfile.close();

}
