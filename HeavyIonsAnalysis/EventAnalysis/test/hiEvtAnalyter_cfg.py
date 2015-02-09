import FWCore.ParameterSet.Config as cms

process = cms.Process('EvtAna')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring('file:/tmp/azsigmon/hiReco_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_RECO_100_1_gMP.root'),
)

process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32(-1))

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc_HIon', '')

process.GlobalTag.toGet.extend([
   cms.PSet(record = cms.string("HeavyIonRcd"),
      tag = cms.string("CentralityTable_HFtowers200_HydjetDrum5_v740x01_mc"),
      connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
      label = cms.untracked.string("HFtowersHydjetDrum5")
   ),
])

process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi") 
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")
process.centralityBin.nonDefaultGlauberModel = cms.string("HydjetDrum5")

process.TFileService = cms.Service("TFileService",
                                  fileName=cms.string("eventtree.root"))

process.load('GeneratorInterface.HiGenCommon.HeavyIon_cff')

#process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')

process.p = cms.Path(process.heavyIon * process.centralityBin * process.hiEvtAnalyzer)
