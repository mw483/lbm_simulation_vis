#! /bin/sh

export OMP_NUM_THREADS=12
 
./src/run_analysis \
  -NUM_RANK				400		\		number of rank
	-X_NUM_RANK			20		\		number of rank in x direction
	-Y_NUM_RANK			20		\		number of rank in y direction
	-X_RANK					480		\		grid number in x direction par rank
	-Y_RANK					120		\		grid number in y direction par rank
	-X_DOMAIN				9600	\		grid number of global map in x direction
	-Y_DOMAIN				2400	\		grid number of global map in y direction
	-Z_DOMAIN				500		\		grid number of global map in z direction
	-dX							2.0		\		resolution
	-dT							0.008	\		timestep
	-FILE_START			1000	\	 	start file number  	
	-FILE_END				1190	\ 	end file number
	-POUT						125		\		pout in runlbm.sh or mpirun.sh
	-PGEN_STEP			125		\		generate_step in runlbm.sh or mpirun.sh
	-NUM_GEN				600		\		number of particle generation par source
	-FLG_NUM				0			\		calculation of total number in domain
	-FLG_DENSITY		0			\		calculation of density (sum)
	-FLG_PROFILE		0			\		calculation of profile (sum)
	-FLG_FOOT			 	0			\		calculation of footprint
	-FLG_FLUX				0			\		calculation of flux	
	-FLG_RESID			1			\		calculation of residential time

	// Setting for density
	-N_XY						3			\		number of plane for density of xy plane 
	-Z_OUT					5 15 25 \ center of plane [m]
	-N_XZ						3			\		number of plane for density of xz plane
	-Y_OUT					1200 2400 3600\ center of plane [m]
	-N_YZ						3			\		number of plane for denisty of yz plane
	-X_OUT					11520 15360 19100\	center of plane [m]
	-H_AVE					10		\		width of plane for density

	// Setting for footprint
	-N_SOURCE				30195 \		number of source
	-ID_DIGIT				4			\ 	number of "0" in particle index (if id == 1120000, ID_DIGIT = 4)
	-N_SENSOR				3			\		number of sensor
	-CTR_SENSOR			18000.0	2400.0 	10.0 \	coordinate of sensor (x, y, z) [m]
									18000.0	2400.0 	20.0 \	"
									18000.0	2400.0	30.0 \	"
	-SIZE_SENSOR		100.0 100.0 10.0 \	size of sensor (dx, dy, dz) [m]

	// Setting for flux
	-N_FLUX					1			\		number of plane		
	-Z_FLUX					10.0	\		height of plane [m]

	// Setting for residence time
	-Z_RESID				10.0 	\		height of plane [m]

	// directry
	-DIR_DATA				../DATA_20210216_garuda/particle/	\ 	particle data 
	-DIR_OUT				./Output_tmp	\												output folder
	-FNAME_MAP			./map/garuda_9600_2400_topo_fill		\	map file 
	-FNAME_SOURCE   ./particle_position/particle_position.txt \ source file 
	| tee	-a				./log_analysis.txt										logfile of analysis
