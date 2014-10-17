#include "TTree.h"
#include "TFile.h"
#include "TStopwatch.h"
#include "TChain.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TCanvas.h"
#include <vector>
#include <iostream>

double FindCentWeight(int bin)
{

 const int nbins = 100;
 double Weight[nbins] = {1.038, 0.8481, 0.8557, 0.9183, 1.025, 1.01, 1.079, 1.185, 1.086, 1.111, 1.202, 1.286, 1.265, 1.181, 1.226, 1.325, 1.308, 1.25, 1.309, 1.23, 1.075, 1.275, 1.226, 1.249, 1.217, 1.172, 1.214, 1.152, 1.201, 0.9944, 1.206, 1.18, 1.126, 1.211, 1.204, 1.027, 1.079, 1.197, 1.035, 0.997, 1.017, 0.9042, 1.114, 0.9512, 1.043, 0.9834, 0.9414, 0.9494, 0.9534, 0.9288, 0.8927, 0.8319, 0.8161, 0.83, 0.6661, 0.7485, 0.7318, 0.6947, 0.7192, 0.7434, 0.792, 0.7013, 0.6677, 0.6113, 0.606, 0.6313, 0.5392, 0.6364, 0.7054, 0.5847, 0.5939, 0.7224, 0.6579, 0.5694, 0.4801, 0.4285, 0.5936, 0.4399, 0.5152, 0.6814, 0.4369, 0.6442, 0.3553, 0.4977, 0.4458, 0.4034, 0.4401, 0.7277, 0.6237, 0.4963, 0.5874, 0.7099, 0.7775, 1.273, 1.539, 1.652, 1.054, 2.553, 0, 0};

 int i = bin/(100/nbins);
 return Weight[i];

}

double FindVtxWeight(double x)
{
 double ww = (0.150412*exp(-0.5*((x+0.0618782)/5.35538)*((x+0.0618782)/5.35538))) / (0.0929117*exp(-0.5*((x-0.466586)/9.62938)*((x-0.466586)/9.62938)));
 return ww;
}

void addWeights(TString treeName="tpTreeSta", TString cut = "") {
    if (gROOT->GetListOfFiles()->GetSize() < 1) {
        std::cerr << "USAGE: root -b -l -q mcFile.root addWeights.C+" << std::endl;
        return;
    }
    std::cout << "Gathering trees ..." << std::endl;
    TTree  &tMC = * (TTree *) ((TFile*)gROOT->GetListOfFiles()->At(0))->Get(treeName+"/fitter_tree");

    std::cout << "Adding weight column ..." << std::endl;
    Float_t zVtx, weight;
    Int_t cBin;
    tMC.SetBranchAddress("event_PrimaryVertex_z", &zVtx);
    tMC.SetBranchAddress("event_hiBin", &cBin);
    TFile *fOut = new TFile("tnpZ_withWeights_pPb_MCembedded_v5.root", "update");
    fOut->mkdir(treeName)->cd();
    TTree *tOut = tMC.CloneTree(0);
    tOut->Branch("weight", &weight, "weight/F");
    int step = tMC.GetEntries()/100;
    double evDenom = 100.0/double(tMC.GetEntries());
    TStopwatch timer; timer.Start();
    for (int i = 0, n = tMC.GetEntries(); i < n; ++i) {
        tMC.GetEntry(i);
        weight = FindVtxWeight(zVtx)*FindCentWeight(cBin);
        tOut->Fill();
        if ((i+1) % step == 0) { 
            double totalTime = timer.RealTime()/60.; timer.Continue();
            double fraction = double(i+1)/double(n+1), remaining = totalTime*(1-fraction)/fraction;
            printf("Done %9d/%9d   %5.1f%%   (elapsed %5.1f min, remaining %5.1f min)\n", i, n, i*evDenom, totalTime, remaining); 
            fflush(stdout); 
        }
    }

    tOut->AutoSave(); // according to root tutorial this is the right thing to do

    std::cout << "Wrote output to " << fOut->GetName() << std::endl;
    fOut->Close();

}
