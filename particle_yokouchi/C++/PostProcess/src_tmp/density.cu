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

#include "stSetting.h"
#include "density.h"

void ParticleDensity::allocate_density (Setting& setting) {
	// Copy setting
	const int x_domain = setting.X_DOMAIN;
	const int y_domain = setting.Y_DOMAIN;
	const int n_slice  = setting.N_XY;
	
	// Allocate
	std::cout << "Allocate density memory -----" << std::endl;
	number_density = new int[n_slice*y_domain*x_domain];
	
	// Initialization
	for (int i=0; i<n_slice; i++) {
		for (int j=0; j<y_domain; j++) {
			for (int k=0; k<x_domain; k++) {
				number_density[k+j*x_domain+i*x_domain*y_domain] = 0;
			}
		}
	}
}

void ParticleDensity::cal_density (float x, float y, float z, Setting& setting) {
	// Copy setting
	const int	x_domain  = setting.X_DOMAIN;
	const int y_domain	= setting.Y_DOMAIN;
	const int n_slice 	= setting.N_XY;
	const float dx 			= setting.dX;
	const float h_ave		= setting.H_AVE;
			  float z_out[n_slice];
	std::copy(setting.Z_OUT, setting.Z_OUT+n_slice, z_out);

	// cal
	for (int i=0; i<n_slice; i++) {
		float z_ctr = z_out[i];
		float z_min = z_ctr - h_ave / 2;
		float z_max = z_ctr + h_ave / 2;

		if (x < 0.0) x = 0.0;
		if (y < 0.0) y = 0.0;
		if (z < 0.0) z = 0.0;

		if (z_min < z && z < z_max) {
			int x_index = (int)(x/dx);
			int y_index = (int)(y/dx);
			number_density[x_index+y_index*x_domain+i*y_domain*x_domain]++;
		}
	}
}

void ParticleDensity::output_density (Setting& setting) {
	// Copy setting
	const int x_domain 	= setting.X_DOMAIN;
	const int y_domain 	= setting.Y_DOMAIN;
	const int n_slice  	= setting.N_XY;
	const char*	dir_out = setting.DIR_OUT;
			float z_out[n_slice];
	std::copy(setting.Z_OUT, setting.Z_OUT+n_slice, z_out);

	// Output
	for (int i=0; i<n_slice; i++) {
		float zi_out = z_out[i];

		std::cout << "Output density (" << zi_out << ") >>>>> ";
		std::fstream	dFile;
		char					densityFile[100];

		sprintf(densityFile, "./%s/number_density_%dm.csv", dir_out, (int)zi_out);
		dFile.open(densityFile, std::ios::out);
		if (!dFile.is_open()) {
			std::cout << "cannot open the output file" << std::endl;
			std::cout << "File (density file)" << std::endl;
			exit(EXIT_FAILURE);
		}
		for (int j=0; j<y_domain; j++) {
			for (int k=0; k<x_domain; k++) {
				dFile << number_density[k+j*x_domain+i*y_domain*x_domain];
				if (k<x_domain-1) dFile << ",";
			}
			dFile << std::endl;
		}
		dFile.close();
		std::cout << "Finish!!" << std::endl;
	}
}

void ParticleDensity::delete_density () {
	delete[] number_density;
}
