import FWCore.ParameterSet.Config as cms

from RecoPixelVertexing.PixelLowPtUtilities.common_cff     import *
from RecoPixelVertexing.PixelLowPtUtilities.firstStep_cff  import *
from RecoPixelVertexing.PixelLowPtUtilities.secondStep_cff import *
from RecoPixelVertexing.PixelLowPtUtilities.thirdStep_cff  import *

#from RecoVZero.VZeroFinding.VZeros_cff import *

###################################
# First step, triplets, r=0.2 cm
firstStep  = cms.Sequence(firstLayerTriplets
                        * pixel3ProtoTracks
                        * pixel3Vertices
                        * firstLayerTriplets
                        * pixel3PrimTracks
                        * primSeeds
                        * primTrackCandidates
                        * globalPrimTracks)

###################################
# Second step, triplets, r=3.5 cm
secondStep = cms.Sequence(secondClusters
                        * secondLayerTriplets
                        * pixelSecoTracks
                        * secoSeeds
                        * secoTrackCandidates
                        * globalSecoTracks)

###################################
# Third step, pairs, not used
thirdStep  = cms.Sequence( thirdClusters
                         * thirdLayerPairs
                         * pixelTertTracks
                         * tertSeeds
                         * tertTrackCandidates
                         * globalTertTracks)

###################################
# Tracklist combiner
allTracks = cms.EDProducer("TrackListCombiner",
    trackProducers = cms.vstring('globalPrimTracks',
                                 'globalSecoTracks',
                                 'globalTertTracks')
)

###################################
# Minimum bias tracking
minBiasTracking = cms.Sequence(firstStep
                            * secondStep
                             * thirdStep 
                             * allTracks)
