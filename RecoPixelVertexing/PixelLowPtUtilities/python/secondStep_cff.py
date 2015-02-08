import FWCore.ParameterSet.Config as cms

#################################
# Remaining clusters
secondClusters = cms.EDProducer("TrackClusterRemover",
    trajectories = cms.InputTag("globalPrimTracks"),
    pixelClusters = cms.InputTag("siPixelClusters"),
    maxChi2 = cms.double(999999.0),
    stripClusters = cms.InputTag("siStripClusters"),
    clusterLessSolution = cms.bool(True)
)

#################################
# Secondary triplets
from RecoPixelVertexing.PixelLowPtUtilities.common_cff import BPixError
from RecoPixelVertexing.PixelLowPtUtilities.common_cff import FPixError
secondLayerTriplets = cms.EDProducer("SeedingLayersEDProducer",
    layerList = cms.vstring('BPix1+BPix2+BPix3',
        'BPix1+BPix2+FPix1_pos',
        'BPix1+BPix2+FPix1_neg',
        'BPix1+FPix1_pos+FPix2_pos',
        'BPix1+FPix1_neg+FPix2_neg'),
    BPix = cms.PSet(
        BPixError,
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
        skipClusters = cms.InputTag('secondClusters')
    ),
    FPix = cms.PSet(
        FPixError,
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
        skipClusters = cms.InputTag('secondClusters')
    )
)

#################################
# Pixel-3 secondary tracks
import RecoPixelVertexing.PixelLowPtUtilities.AllPixelTracks_cfi
pixelSecoTracks = RecoPixelVertexing.PixelLowPtUtilities.AllPixelTracks_cfi.allPixelTracks.clone()
pixelSecoTracks.passLabel = 'Pixel triplet tracks without vertex constraint'
pixelSecoTracks.RegionFactoryPSet.RegionPSet.originRadius = 3.5
pixelSecoTracks.OrderedHitsFactoryPSet.SeedingLayers = 'secondLayerTriplets'

#################################
# Secondary seeds
import RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi
secoSeeds = RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi.pixelTrackSeeds.clone()
secoSeeds.InputCollection = 'pixelSecoTracks'

#################################
# Secondary measurement tracker
import RecoTracker.MeasurementDet.MeasurementTrackerESProducer_cfi
secondMeasurementTracker = RecoTracker.MeasurementDet.MeasurementTrackerESProducer_cfi.MeasurementTracker.clone()
secondMeasurementTracker.ComponentName        = 'secondMeasurementTracker'

#################################
# Secondary trajectory builder
import RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi
secondCkfTrajectoryBuilder = RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi.GroupedCkfTrajectoryBuilder.clone()
#secondCkfTrajectoryBuilder.ComponentName      = 'secondCkfTrajectoryBuilder'
secondCkfTrajectoryBuilder.MeasurementTrackerName = 'secondMeasurementTracker'
secondCkfTrajectoryBuilder.trajectoryFilter   = cms.PSet(refToPSet_ = cms.string('MinBiasCkfTrajectoryFilter'))
secondCkfTrajectoryBuilder.inOutTrajectoryFilter  = cms.PSet(refToPSet_ = cms.string('MinBiasCkfTrajectoryFilter'))
secondCkfTrajectoryBuilder.clustersToSkip = cms.InputTag('secondClusters')

#################################
# Secondary track candidates
import RecoTracker.CkfPattern.CkfTrackCandidates_cfi
secoTrackCandidates = RecoTracker.CkfPattern.CkfTrackCandidates_cfi.ckfTrackCandidates.clone()
secoTrackCandidates.TrajectoryBuilder    = 'secondCkfTrajectoryBuilder'
secoTrackCandidates.TrajectoryCleaner    = 'TrajectoryCleanerBySharedSeeds'
secoTrackCandidates.src                  = 'secoSeeds'
secoTrackCandidates.RedundantSeedCleaner = 'none'
secoTrackCandidates.useHitsSplitting          = cms.bool(False)
secoTrackCandidates.doSeedingRegionRebuilding = cms.bool(False)

#################################
# Global secondary tracks
import RecoTracker.TrackProducer.CTFFinalFitWithMaterial_cfi
globalSecoTracks = RecoTracker.TrackProducer.CTFFinalFitWithMaterial_cfi.ctfWithMaterialTracks.clone()
globalSecoTracks.src                = 'secoTrackCandidates'
globalSecoTracks.TrajectoryInEvent  = cms.bool(True)

