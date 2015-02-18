#ifndef TkSeedingLayers_SeedingHitSet_H
#define TkSeedingLayers_SeedingHitSet_H

#include "DataFormats/TrackerRecHit2D/interface/BaseTrackerRecHit.h"

#include <vector>

class SeedingHitSet {
public:

  using      RecHit        = BaseTrackerRecHit;
  using      RecHitPointer = BaseTrackerRecHit *;
  using ConstRecHitPointer = BaseTrackerRecHit const *;

  static ConstRecHitPointer nullPtr() { return nullptr;}

  SeedingHitSet()
  {
    for(unsigned int i = 0; i < 10; i++)
      theRecHits[i]=nullptr;
  }

// MODIFICATION STARTS HERE
  SeedingHitSet(ConstRecHitPointer one, ConstRecHitPointer two) 
  {
    theRecHits[0]=one;
    theRecHits[1]=two;

    for(unsigned int i = 2; i < 10; i++)
      theRecHits[i]=nullptr;
  }
  SeedingHitSet(ConstRecHitPointer  one, ConstRecHitPointer  two, 
		ConstRecHitPointer three) 
  {
    theRecHits[0]=one;
    theRecHits[1]=two;
    theRecHits[2]=three;

    for(unsigned int i = 3; i < 10; i++)
      theRecHits[i]=nullptr;
  }

  SeedingHitSet(ConstRecHitPointer one, ConstRecHitPointer two,
                ConstRecHitPointer three, ConstRecHitPointer four)
  {
    theRecHits[0]=one;
    theRecHits[1]=two;
    theRecHits[2]=three;
    theRecHits[3]=four;

    for(unsigned int i = 4; i < 10; i++)
      theRecHits[i]=nullptr;
  }
  
  SeedingHitSet(std::vector<ConstRecHitPointer> & hits)
  {
    for(unsigned int i = 0; i < hits.size(); i++)
      theRecHits[i] = hits[i];

    for(unsigned int i = hits.size() ; i < 10; i++)
      theRecHits[i]=nullptr;
  }

  unsigned int size() const
  {
    for(unsigned int i = 0; i < 10; i++)
      if(! theRecHits[i])
        return (i > 1 ? i : 0);

    return 10;
  }

  void set(unsigned int i, ConstRecHitPointer & hit)
  {
    theRecHits[i] = hit;
  }
// MODIFICATION ENDS HERE 

  ConstRecHitPointer  get(unsigned int i) const { return theRecHits[i]; }
  ConstRecHitPointer  operator[](unsigned int i) const { return theRecHits[i]; }
  
private:
// MODIFICATION STARTS HERE 
  ConstRecHitPointer theRecHits[10]; // was 4
// MODIFICATION ENDS HERE 
};


#endif
