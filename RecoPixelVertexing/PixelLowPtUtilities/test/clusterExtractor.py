import FWCore.ParameterSet.Config as cms

process = cms.Process("ClusterShape")

process.load("Configuration.StandardSequences.Services_cff")
process.load("SimGeneral.MixingModule.mixNoPU_cfi")
process.load("Configuration.StandardSequences.Simulation_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.RawToDigi_cff")

process.load("SimGeneral.TrackingAnalysis.trackingParticles_cfi")
process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")

process.load("RecoLocalTracker.Configuration.RecoLocalTracker_cff")

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("RecoPixelVertexing.PixelLowPtUtilities.MinBiasTracking_cff")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

###############################################################################
# Message logger
process.MessageLogger = cms.Service("MessageLogger",
     categories = cms.untracked.vstring(
      'MinBiasTracking'
    ),
    debugModules = cms.untracked.vstring('*'),
     cerr = cms.untracked.PSet(
         threshold = cms.untracked.string('DEBUG'),
#        threshold = cms.untracked.string('ERROR'),
         DEBUG = cms.untracked.PSet(
             limit = cms.untracked.int32(0)
         )
     ),
     destinations = cms.untracked.vstring('cerr'),
     suppressWarning = cms.untracked.vstring('siStripZeroSuppression')
)

###############################################################################
# Source
process.source = cms.Source("PoolSource",
    skipEvents = cms.untracked.uint32(0),
    fileNames  = cms.untracked.vstring(
       # /RelValMinBias/*/GEN-SIM-DIGI-RAW-HLTDEBUG
       'file:///tmp/sikler/820E70BE-F39D-E411-80BA-0025905A6138.root',
       'file:///tmp/sikler/8E5AC8DC-FC9D-E411-AE20-003048FFD770.root',
       'file:///tmp/sikler/9805E1CF-F59D-E411-B3F1-003048FFCB9E.root')
)

process.maxEvents = cms.untracked.PSet(
     input = cms.untracked.int32(10000)
#    input = cms.untracked.int32(10)
)

###############################################################################
# Cluster shape
process.clusterShape = cms.EDAnalyzer("ClusterShapeExtractor",
    trackProducer  = cms.string('allTracks'),
    clusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
    hasSimHits     = cms.bool(True),
    hasRecTracks   = cms.bool(False),
    associateStrip      = cms.bool(True),
    associatePixel      = cms.bool(True),
    associateRecoTracks = cms.bool(False),
    ROUList = cms.vstring(
      'TrackerHitsTIBLowTof', 'TrackerHitsTIBHighTof',
      'TrackerHitsTIDLowTof', 'TrackerHitsTIDHighTof',
      'TrackerHitsTOBLowTof', 'TrackerHitsTOBHighTof',
      'TrackerHitsTECLowTof', 'TrackerHitsTECHighTof',
      'TrackerHitsPixelBarrelLowTof',
      'TrackerHitsPixelBarrelHighTof',
      'TrackerHitsPixelEndcapLowTof',
      'TrackerHitsPixelEndcapHighTof')
)

process.load("RecoPixelVertexing.PixelLowPtUtilities.siPixelClusterShapeCache_cfi")

process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")

process.load("RecoLocalTracker.SiPixelClusterizer.SiPixelClusterizer_cfi")
process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")

###############################################################################
# Paths
process.simu  = cms.Path(process.mix
#                      * process.trackingParticles
                       * process.offlineBeamSpot)

process.digi  = cms.Path(process.RawToDigi)

#process.lreco = cms.Path(process.trackerlocalreco
#                       * process.clusterShape)

process.lreco = cms.Path(process.trackerlocalreco
                       * process.siPixelClusters
                       * process.siPixelRecHits
                       * process.MeasurementTrackerEvent
                       * process.siPixelClusterShapeCache
                       * process.clusterShape)

###############################################################################
# Global tag
process.GlobalTag.globaltag = 'MCRUN2_73_V9::All'

###############################################################################
# Schedule
process.schedule = cms.Schedule(process.simu,
                                process.digi,
                                process.lreco)

