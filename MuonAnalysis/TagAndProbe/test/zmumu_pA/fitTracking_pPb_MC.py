import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TnP_Tracking = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
     ## Input, output 
    InputFileNames = cms.vstring("file:tnpZ_withWeights_pPb_MC_Powheg_TuneZ2star_v6.root"),
    OutputFileName = cms.string("fits2_Tracking_dR_vtxWeights_pPb_MC_Powheg_Voigt4Exp.root"),
    InputTreeName = cms.string("fitter_tree"), 
    InputDirectoryName = cms.string("tpTreeSta"),  
    WeightVariable = cms.string("weight"),
    ## Variables for binning
    Variables = cms.PSet(
        mass = cms.vstring("Tag-Probe Mass", "40", "140", "GeV/c^{2}"),
        pt     = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("Probe #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("Probe |#eta|", "0", "2.5", ""),
        phi    = cms.vstring("Probe #phi", "-3.1416", "3.1416", ""),
        tag_pt = cms.vstring("Tag p_{T}", "2.6", "1000", "GeV/c"),
        tk_deltaR   = cms.vstring("Match #Delta R",    "0", "1000", ""),
        tk_deltaEta = cms.vstring("Match #Delta #eta", "0", "1000", ""),
        tk_deltaR_NoZ   = cms.vstring("Unmatch #Delta R",    "0", "1000", ""),
        tk_deltaEta_NoZ = cms.vstring("Unmatch #Delta #eta", "0", "1000", ""),
	event_hiBin	= cms.vstring("Centrality bin", "0", "100", ""),
	weight = cms.vstring("weight","0","10",""),
    ),
    ## Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
	TrackerMu = cms.vstring("Tracker muon", "dummy[pass=1,fail=0]"),
	tag_PAMu12 = cms.vstring("HLT_PAMu12", "dummy[pass=1,fail=0]"),
        outerValidHits = cms.vstring("hasValidHits", "dummy[pass=1,fail=0]"),
    ),
    Cuts = cms.PSet(
	dr_cut = cms.vstring("track deltaR matching", "tk_deltaR", "0.3"),
	deta_cut = cms.vstring("track deltaEta matching", "tk_deltaEta", "0.3"),
    ),
    ## What to fit
    Efficiencies = cms.PSet(
        Trk_pt = cms.PSet(
            UnbinnedVariables = cms.vstring("mass","weight"),
            EfficiencyCategoryAndState = cms.vstring("dr_cut","below"), ## Numerator definition
            BinnedVariables = cms.PSet(
                ## Binning in continuous variables
                eta = cms.vdouble(-2.4, 2.4),
                pt = cms.vdouble( 10, 20, 30, 40, 50, 70, 100 ),
		event_hiBin = cms.vdouble(0,100),
                ## flags and conditions required at the denominator, 
                tag_PAMu12 = cms.vstring("pass"), ## i.e. use only events for which this flag is true
		outerValidHits = cms.vstring("pass"),
            ),
            BinToPDFmap = cms.vstring("Voigt4Exp"), ## PDF to use, as defined below
        ),
        Trk_eta = cms.PSet(
            UnbinnedVariables = cms.vstring("mass","weight"),
            EfficiencyCategoryAndState = cms.vstring("dr_cut","below"), ## Numerator definition
            BinnedVariables = cms.PSet(
                eta = cms.vdouble(-2.4, -2.1, -1.6, -1.1, -0.6, 0, 0.6, 1.1, 1.6, 2.1, 2.4),
                pt = cms.vdouble(20, 100),
		event_hiBin = cms.vdouble(0,100),
                tag_PAMu12 = cms.vstring("pass"),
		outerValidHits = cms.vstring("pass"),
            ),
            BinToPDFmap = cms.vstring("Voigt4Exp"), ## PDF to use, as defined below
        ),
        Trk_1bin = cms.PSet(
            UnbinnedVariables = cms.vstring("mass","weight"),
            EfficiencyCategoryAndState = cms.vstring("dr_cut","below"), ## Numerator definition
            BinnedVariables = cms.PSet(
                eta = cms.vdouble(-2.4, 2.4),
                pt = cms.vdouble(20, 100),
		event_hiBin = cms.vdouble(0,100),
                tag_PAMu12 = cms.vstring("pass"),
		outerValidHits = cms.vstring("pass"),
            ),
            BinToPDFmap = cms.vstring("Voigt4Exp"), ## PDF to use, as defined below
        ),
#        Trk_cent = cms.PSet(
#            UnbinnedVariables = cms.vstring("mass","weight"),
#            EfficiencyCategoryAndState = cms.vstring("dr_cut","pass"), ## Numerator definition
#            BinnedVariables = cms.PSet(
#                eta = cms.vdouble(-2.4, 2.4),
#                pt = cms.vdouble(20, 100),
#                event_hiBin = cms.vdouble(0,10,20,50,100),
#                tag_PAMu12 = cms.vstring("pass"),
#		outerValidHits = cms.vstring("pass"),
#            ),
#            BinToPDFmap = cms.vstring("Voigt4Exp"), ## PDF to use, as defined below
#        ),
    ),

    ## PDF for signal and background (double voigtian + exponential background)
    PDFs = cms.PSet(
	Voigt2Exp = cms.vstring(
		"Voigtian::signal1(mass, mean1[101,85,125], width1[3,1,10], sigma1[3,1,10])",
		"Voigtian::signal2(mass, mean2[81,65,95], width2[3,1,10], sigma2[3,1,10])",
		"SUM::signal(signal1,factor[0.1,0,10]*signal2)",
		"Exponential::backgroundPass(mass, lp[0,-5,5])",
		"Exponential::backgroundFail(mass, lf[0,-5,5])",
        	"efficiency[0.9,0,1]",
        	"signalFractionInPassing[0.9]"
	),
	BWResCBExp = cms.vstring(
		"BreitWigner::bw(mass, m0[91.2,81.2,101.2], width[2.495,1,10])",
		"RooCBShape::res(mass, peak[0], sigma[1.7,0.01,10], alpha[1.8,0,3], n[0.8,0,10])",
		"FCONV::signal(mass, bw, res)",
		"Exponential::backgroundPass(mass, lp[0,-5,5])",
		"Exponential::backgroundFail(mass, lf[0,-5,5])",
		"efficiency[0.9,0.5,1]",
		"signalFractionInPassing[0.9]",
	),
	Voigt4Exp = cms.vstring(
		"Voigtian::signal1(mass, mean1[101,85,125], width1[3,1,10], sigma1[3,1,10])",
		"Voigtian::signal2(mass, mean2[81,65,95], width2[3,1,10], sigma2[3,1,10])",
		"Voigtian::signal3(mass, mean3[101,85,125], width3[3,1,10], sigma3[3,1,10])",
		"Voigtian::signal4(mass, mean4[81,65,95], width4[3,1,10], sigma4[3,1,10])",
		"SUM::signalPass(signal1,factorPass[0.1,0,10]*signal2)",
		"SUM::signalFail(signal3,factorFail[0.1,0,10]*signal4)",
		"Exponential::backgroundPass(mass, lp[0,-5,5])",
		"Exponential::backgroundFail(mass, lf[0,-5,5])",
        	"efficiency[0.9,0,1]",
        	"signalFractionInPassing[0.9]"
	),
    ),

    ## How to do the fit
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(True),
    NumCPU = cms.uint32(1), ## leave to 1 for now, RooFit gives funny results otherwise
    SaveWorkspace = cms.bool(True),
)

process.p = cms.Path(process.TnP_Tracking)
