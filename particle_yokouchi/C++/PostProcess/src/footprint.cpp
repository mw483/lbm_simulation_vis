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

#include "footprint.h"
#include "stSetting.h"
#include "stParticle.h"
#include "function.h"

/* -------- Class ParticleFootPrint -------- */

int ParticleFootPrint::binary_search_sort (int id, int n_source) {
	int max_index = n_source;
	int min_index = 0;

	int mid_index;
	int t = 0;
	while (true) {
		mid_index = (max_index + min_index) / 2;
		if (p_source[mid_index].index == id) break;
		else if (p_source[mid_index].index > id) max_index = mid_index;
		else min_index = mid_index;

		if (t > n_source) {
			std::cout << "Error!! (Binary search)" << std::endl;
			exit(EXIT_FAILURE);
		}
		t++;
	}
	return mid_index;
}

void ParticleFootPrint::allocate_footprint_source (Setting& setting) {
	// Copy setting
	const int n_source = setting.N_SOURCE;
	const int n_sensor = setting.N_SENSOR;
	
	// Allocate
	std::cout << "Allocate source memory -----" << std::endl;
	p_source  = new Particle_Index[n_source];
}

void ParticleFootPrint::allocate_footprint (Setting& setting) {
	// Copy setting
	const int n_sensor			 = setting.N_SENSOR;
	const int n_source_index = max_index + 1;
	
	// Allocate
	std::cout << "Allocate footprint memory -----" << std::endl;
	footprint 	 = new int[n_sensor*n_source_index];
	num_p_sensor = new int[n_sensor];

	// Initilization
	for (int i=0; i<n_source_index; i++)	{
		footprint[i] = 0;
	}
	for (int i=0; i<n_sensor; i++) {
		num_p_sensor = new int[n_sensor];
	}
}

void ParticleFootPrint::read_source (Setting& setting) {
	// Copy setting
	const int 	n_source 			= setting.N_SOURCE;
	const int 	id_digit			= setting.ID_DIGIT;
	const char*	fname_source 	= setting.FNAME_SOURCE;

	// Read
	std::cout << "Read source data. File name >> " << fname_source <<  std::endl;
	
	std::fstream	sFile;

	sFile.open(fname_source, std::ios::in);
	if(!sFile.is_open()) {
		std::cout << "cannot open source file" << std::endl;
		exit(EXIT_FAILURE);
	}

	int group;
	int index_;
	Particle_Index p_min;
		p_min.index = 10000;
		p_min.pos_x = 0.0;
		p_min.pos_y = 0.0;
		p_min.pos_z = 0.0;

	Particle_Index p_max;
		p_max.index = 0;
		p_max.pos_x = 0.0;
		p_max.pos_y = 0.0;
		p_max.pos_z = 0.0;

	for (int i=0; i<n_source; i++) {
		sFile >> p_source[i].pos_x;
		sFile >> p_source[i].pos_y;
		sFile >> p_source[i].pos_z;
		sFile >> group;
		sFile >> index_;
		p_source[i].index = index_ / pow(10, id_digit);
		
		if (p_min.index > p_source[i].index) {
			p_min.index = p_source[i].index;
			p_min.pos_x = p_source[i].pos_x;
			p_min.pos_y = p_source[i].pos_y;
			p_min.pos_z = p_source[i].pos_z;
		}
		if (p_max.index < p_source[i].index) {
			p_max.index = p_source[i].index;
			p_max.pos_x = p_source[i].pos_x;
			p_max.pos_y = p_source[i].pos_y;
			p_max.pos_z = p_source[i].pos_z;
		}

		if (p_source[i].index <= 0 || n_source < p_source[i].index) {
			std::cout << "Error!! Source data is incorrect.";
		}
	}
	std::cout << " -min::index = " << p_min.index << " (x=" << p_min.pos_x << " y=" << p_min.pos_y  << " z=" << p_min.pos_z << ")" << std::endl;
	std::cout << " -max::index = " << p_max.index << " (x=" << p_max.pos_x << " y=" << p_max.pos_y  << " z=" << p_max.pos_z << ")" << std::endl;
	std::cout << std::endl;

	max_index = p_max.index;
	min_index = p_min.index;

	// sort
	qsort(p_source, n_source, sizeof *p_source, sort_compare);

}

void ParticleFootPrint::cal_footprint (float x, float y, float z, int index, Setting& setting) {
	// Copy setting
	const int 	x_domain		= setting.X_DOMAIN;
	const int 	y_domain		= setting.Y_DOMAIN;
	const float	dx					= setting.dX;
	const int 	n_source 		= setting.N_SOURCE;
	const int		n_sensor		= setting.N_SENSOR;
	const int		id_digit		= setting.ID_DIGIT;
			float 	ctr_sensor[n_sensor*3];
			float 	size_sensor[3];
	std::copy(setting.CTR_SENSOR,		setting.CTR_SENSOR+n_sensor*3, 	ctr_sensor);
	std::copy(setting.SIZE_SENSOR,	setting.SIZE_SENSOR+3, 					size_sensor);

	// cal
	for (int i=0; i<n_sensor; i++) {
		float x_sensor = ctr_sensor[3*i  ];
		float y_sensor = ctr_sensor[3*i+1];
		float z_sensor = ctr_sensor[3*i+2];

		float xs_min	 = x_sensor - size_sensor[0] / 2.0;
		float xs_max	 = x_sensor + size_sensor[0] / 2.0;
		float ys_min	 = y_sensor - size_sensor[1] / 2.0;
		float ys_max	 = y_sensor + size_sensor[1] / 2.0;
		float zs_min	 = z_sensor - size_sensor[2] / 2.0;
		float zs_max	 = z_sensor + size_sensor[2] / 2.0;

		if (xs_min <= x && x <= xs_max && ys_min <= y && y <= ys_max && zs_min <= z && z <= zs_max ) {
			int id_s = index / pow(10, id_digit);
			// int source_index 	= binary_search_sort(id_s, n_source);
			footprint[id_s + i*n_source]++;
			num_p_sensor[i]++;
		}
	}
}

void ParticleFootPrint::output_footprint (Setting& setting) {
	// Copy setting
	const int n_sensor		= setting.N_SENSOR;
	const int n_source		= setting.N_SOURCE;
	const char*	dir_out		= setting.DIR_OUT;
			float	ctr_sensor[n_sensor*3];
	std::copy(setting.CTR_SENSOR,	setting.CTR_SENSOR+n_sensor*3, ctr_sensor);

	// Output
	for (int i=0; i<n_sensor; i++) {
		float x_sensor = ctr_sensor[3*i  ];
		float y_sensor = ctr_sensor[3*i+1];
		float z_sensor = ctr_sensor[3*i+2];

		std::cout << "Output footprint (" << x_sensor << ", " << y_sensor << ", " << z_sensor << ") >>>>> ";
		std::fstream 	fFile;
		char					footFile[100];

		sprintf(footFile, "./%s/footprint_%d_%d_%d.csv", dir_out, (int)x_sensor, (int)y_sensor, (int)z_sensor);
		fFile.open(footFile, std::ios::out);
		if (!fFile.is_open()) {
			std::cout << "cannot open the output file" << std::endl;
			std::cout << "File (footprint file)" << std::endl;
			exit(EXIT_FAILURE);
		}
		
		for (int j=0; j<n_source; j++) {
			fFile <<  j;
			if (j < n_source-1) fFile << ",";
		}
	
		for (int j=0; j<n_source; j++) {
			fFile <<  footprint[j + i*n_source];
			if (j < n_source-1) fFile << ",";
		}
		fFile << std::endl;
	fFile.close();
	std::cout << "Finish!!" << std::endl;
	}
}

void ParticleFootPrint::delete_footprint () {
	delete[] footprint;
	delete[] num_p_sensor;
}

