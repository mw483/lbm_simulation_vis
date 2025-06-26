#ifndef CLASS_FOOTPRINT
#define CLASS_FOOTPRINT

#include <iostream>

#include "stSetting.h"
#include "stParticle.h"

class ParticleFootPrint {
	private:
		int*							footprint;

		int 		binary_search_sort(int id, int n_source, Particle_Index p_source[]);

	public:
		int*		num_p_sensor;

		void		allocate_footprint(Setting& setting);
		void 		read_source(Setting& setting);
		void 		cal_footprint(float x, float y, float z, int index, Setting& setting);
		void		output_footprint(Setting& setting);
		void		delete_footprint();	
};

#endif
