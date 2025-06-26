#include <iostream>
#include <time.h>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include <string.h>
#include <cmath>
#include <stdlib.h>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

#include "residence.h"
#include "stSetting.h"
#include "stParticle.h"

void ParticleResidenceTime::allocate_residence (Setting& setting) {
	// Copy setting 
	const int x_domain = setting.X_DOMAIN;
	const int y_domain = setting.Y_DOMAIN;
	const int n_source = setting.N_SOURCE;

	// Allocate
	residence_particle_h = new float[n_source];
	residence_map      	 = new float[y_domain*x_domain];

	// Allocate device memory
	cudaMalloc(&residence_particle_d, n_source*sizeof(float));

	// Inititialize
	for (int i=0; i<n_source; i++) { 
		residence_particle_h[i] = 0.0;
	}

	// Copy memory host -> device
	cudaMemcpy(residence_particle_d, residence_particle_h, n_source*sizeof(float), cudaMemcpyHostToDevice);	
}

void ParticleResidenceTime::read_source_index (Setting& setting) {
	// Copy setting

}

void ParticleResidenceTime::cal_residence (int t, thrust::host_vector<Particle_Index> p_resid_odd, thrust::host_vector<Particle_Index> p_resid_even,  Setting& setting) {
	// Copy setting
	
}

void ParticleResidenceTime::output_residence (Setting& setting) {

}

void ParticleResidenceTime::delete_residence () {
	delete[] residence_particle_h;
	delete[] residence_map;
	cudaFree(residence_particle_d);
}
