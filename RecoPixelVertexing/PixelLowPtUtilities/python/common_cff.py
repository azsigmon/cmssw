import FWCore.ParameterSet.Config as cms

from RecoLocalTracker.SiPixelRecHits.PixelCPEESProducers_cff import *
from RecoTracker.CkfPattern.CkfTrackCandidates_cff import *
from RecoPixelVertexing.PixelLowPtUtilities.MinBiasCkfTrajectoryFilter_cfi import *
from TrackingTools.TrajectoryCleaning.TrajectoryCleanerBySharedSeeds_cfi import *
from RecoTracker.TrackProducer.CTFFinalFitWithMaterial_cff import *

# Global tracking geometry
GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")

# Transient track builder
TransientTrackBuilderESProducer = cms.ESProducer("TransientTrackBuilderESProducer",
    ComponentName = cms.string('TransientTrackBuilder'),
)

# Pixel barrel errors
BPixError = cms.PSet(
    useErrorsFromParam = cms.bool(True),
    hitErrorRPhi = cms.double(0.0027),
    hitErrorRZ = cms.double(0.006)
)

# Pixel endcap errors
FPixError = cms.PSet(
    useErrorsFromParam = cms.bool(True),
    hitErrorRPhi = cms.double(0.0051),
    hitErrorRZ = cms.double(0.0036)
)

# Trajectory builder
GroupedCkfTrajectoryBuilder.maxCand = 5
GroupedCkfTrajectoryBuilder.intermediateCleaning = False
GroupedCkfTrajectoryBuilder.alwaysUseInvalidHits = False
GroupedCkfTrajectoryBuilder.trajectoryFilter = cms.PSet(refToPSet_ = cms.string('MinBiasCkfTrajectoryFilter'))
GroupedCkfTrajectoryBuilder.inOutTrajectoryFilter = cms.PSet(refToPSet_ = cms.string('MinBiasCkfTrajectoryFilter'))
GroupedCkfTrajectoryBuilder.useSameTrajFilter = cms.bool(True)
 
# Propagator, pion mass
MaterialPropagator.Mass          = cms.double(0.139)
OppositeMaterialPropagator.Mass  = cms.double(0.139)
RungeKuttaTrackerPropagator.Mass = cms.double(0.139)

