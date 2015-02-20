import FWCore.ParameterSet.Config as cms

ClusterShapeHitFilterESProducer = cms.ESProducer("ClusterShapeHitFilterESProducer",
                                                        ComponentName = cms.string('ClusterShapeHitFilter'),
                                                        PixelShapeFile= cms.string('RecoPixelVertexing/PixelLowPtUtilities/data/pixelShape.par'),
# MODIFICATION STARTS HERE
                                                        StripShapeFile= cms.string('RecoPixelVertexing/PixelLowPtUtilities/data/stripShape.par')
# MODIFICATION ENDS HERE
                                                        )
