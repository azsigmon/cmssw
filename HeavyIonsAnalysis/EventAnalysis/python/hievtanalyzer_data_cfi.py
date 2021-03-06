import FWCore.ParameterSet.Config as cms

hiEvtAnalyzer = cms.EDAnalyzer('HiEvtAnalyzer',
   CentralitySrc    = cms.InputTag("hiCentrality"),
   CentralityBinSrc = cms.InputTag("centralityBin","HFtowers"),
   EvtPlane         = cms.InputTag("hiEvtPlane","recoLevel"),
   EvtPlaneFlat     = cms.InputTag("hiEvtPlaneFlat",""),   
   HiMC             = cms.InputTag("heavyIon"),                            
   Vertex           = cms.InputTag("hiSelectedVertex"),
   doCentrality     = cms.bool(True),
   doEvtPlane       = cms.bool(True),
   doEvtPlaneFlat   = cms.bool(False),                               
   doVertex         = cms.bool(True),
   doMC             = cms.bool(False)
)
