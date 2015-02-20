import FWCore.ParameterSet.Config as cms

from RecoTracker.TkSeedingLayers.PixelLayerTriplets_cfi import *
import RecoPixelVertexing.PixelLowPtUtilities.AllPixelTracks_cfi

from RecoPixelVertexing.PixelLowPtUtilities.common_cff import BPixError
from RecoPixelVertexing.PixelLowPtUtilities.common_cff import FPixError
firstLayerTriplets = cms.EDProducer("SeedingLayersEDProducer",
    layerList = cms.vstring(
        'BPix1+BPix2+BPix3',
        'BPix1+BPix2+FPix1_pos',
        'BPix1+BPix2+FPix1_neg',
        'BPix1+FPix1_pos+FPix2_pos',
        'BPix1+FPix1_neg+FPix2_neg'),
    BPix = cms.PSet(
        BPixError,
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
    ),
    FPix = cms.PSet(
        FPixError,
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
    )
)

############################
# Pixel-3 proto tracks
pixel3ProtoTracks = RecoPixelVertexing.PixelLowPtUtilities.AllPixelTracks_cfi.allPixelTracks.clone()
pixel3ProtoTracks.passLabel = 'Pixel triplet tracks for vertexing'

# FIXME
pixel3ProtoTracks.RegionFactoryPSet.ptMin = cms.double(0.2)

############################
# Pixel vertexing
import UserCode.FerencSiklerVertexing.NewVertexProducer_cfi
pixel3Vertices = UserCode.FerencSiklerVertexing.NewVertexProducer_cfi.newVertices.clone()
pixel3Vertices.TrackCollection = 'pixel3ProtoTracks'
 
############################
# Pixel-3 primary tracks
pixel3PrimTracks  = RecoPixelVertexing.PixelLowPtUtilities.AllPixelTracks_cfi.allPixelTracks.clone()
pixel3PrimTracks.passLabel  = 'Pixel triplet tracks with vertex constraint'
pixel3PrimTracks.RegionFactoryPSet.RegionPSet.useFoundVertices = cms.bool(True)

############################
# Primary seeds
import RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi
primSeeds = RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi.pixelTrackSeeds.clone()
primSeeds.InputCollection = 'pixel3PrimTracks'

############################
# Primary track candidates
import RecoTracker.CkfPattern.CkfTrackCandidates_cfi
primTrackCandidates = RecoTracker.CkfPattern.CkfTrackCandidates_cfi.ckfTrackCandidates.clone()
primTrackCandidates.TrajectoryCleaner    = 'TrajectoryCleanerBySharedSeeds'
primTrackCandidates.src                  = 'primSeeds'
primTrackCandidates.RedundantSeedCleaner = 'none'
primTrackCandidates.useHitsSplitting          = cms.bool(False)
primTrackCandidates.doSeedingRegionRebuilding = cms.bool(False)

############################
# Global primary tracks
import RecoTracker.TrackProducer.CTFFinalFitWithMaterial_cfi
globalPrimTracks = RecoTracker.TrackProducer.CTFFinalFitWithMaterial_cfi.ctfWithMaterialTracks.clone()
globalPrimTracks.src               = 'primTrackCandidates'
globalPrimTracks.TrajectoryInEvent = cms.bool(True)
globalPrimTracks.MinNumberOfHits   = cms.int32(3)

