#include "RecoPixelVertexing/PixelLowPtUtilities/interface/ClusterShapeHitFilterESProducer.h"

#include "RecoPixelVertexing/PixelLowPtUtilities/interface/ClusterShapeHitFilter.h"

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "RecoTracker/Record/interface/CkfComponentsRecord.h"


#include "FWCore/MessageLogger/interface/MessageLogger.h"

/*****************************************************************************/
ClusterShapeHitFilterESProducer::ClusterShapeHitFilterESProducer
  (const edm::ParameterSet& iConfig):
// MODIFICATION STARTS HERE
  use_PixelShapeFile( iConfig.exists("PixelShapeFile")?iConfig.getParameter<std::string>("PixelShapeFile"):"RecoPixelVertexing/PixelLowPtUtilities/data/pixelShape.par"),
  use_StripShapeFile( iConfig.exists("StripShapeFile")?iConfig.getParameter<std::string>("StripShapeFile"):"RecoPixelVertexing/PixelLowPtUtilities/data/stripShape.par")
// MODIFICATION ENDS HERE
{
  
  std::string componentName = iConfig.getParameter<std::string>("ComponentName");
  cutOnPixelCharge_ = iConfig.exists("minGoodPixelCharge");
  cutOnStripCharge_ = iConfig.exists("minGoodStripCharge");
  minGoodPixelCharge_= (cutOnPixelCharge_ ? iConfig.getParameter<double>("minGoodPixelCharge") : 0); 
  minGoodStripCharge_= (cutOnStripCharge_ ? iConfig.getParameter<double>("minGoodStripCharge") : 0);
  cutOnPixelShape_ = (iConfig.exists("doPixelShapeCut") ? iConfig.getParameter<bool>("doPixelShapeCut") : true);
  cutOnStripShape_ = (iConfig.exists("doStripShapeCut") ? iConfig.getParameter<bool>("doStripShapeCut") : true);

  edm::LogInfo("ClusterShapeHitFilterESProducer")
    << " with name: "            << componentName;
      
  setWhatProduced(this, componentName);
}


/*****************************************************************************/
ClusterShapeHitFilterESProducer::~ClusterShapeHitFilterESProducer
  ()
{
}

/*****************************************************************************/
ClusterShapeHitFilterESProducer::ReturnType
ClusterShapeHitFilterESProducer::produce
(const ClusterShapeHitFilter::Record &iRecord)
{
  using namespace edm::es;

  // get all from SiStripLorentzAngle (why not!)

  // Retrieve magnetic field
  edm::ESHandle<MagneticField> field;
  iRecord.getRecord<TkStripCPERecord>().getRecord<IdealMagneticFieldRecord>().get(field);

  // Retrieve geometry
  edm::ESHandle<TrackerGeometry> geo;
  iRecord.getRecord<TkStripCPERecord>().getRecord<TrackerDigiGeometryRecord>().get(geo);

  // Retrieve pixel Lorentz
  edm::ESHandle<SiPixelLorentzAngle> pixel;
  iRecord.getRecord<TkPixelCPERecord>().getRecord<SiPixelLorentzAngleRcd>().get(pixel);

  // Retrieve strip Lorentz
  edm::ESHandle<SiStripLorentzAngle> strip;
  iRecord.getRecord<TkStripCPERecord>().getRecord<SiStripLorentzAngleDepRcd>().get(strip);
 


  // Produce the filter using the plugin factory
  ClusterShapeHitFilterESProducer::ReturnType
    aFilter(new ClusterShapeHitFilter(  geo.product(),
                                      field.product(),
                                      pixel.product(),
                                      strip.product(),
// MODIFICATION STARTS HERE
                                      &use_PixelShapeFile,
                                      &use_StripShapeFile));
// MODIFICATION ENDS HERE
  aFilter->setShapeCuts(cutOnPixelShape_, cutOnStripShape_);
  aFilter->setChargeCuts(cutOnPixelCharge_, minGoodPixelCharge_, cutOnStripCharge_,
    minGoodStripCharge_);
  return aFilter;
}
