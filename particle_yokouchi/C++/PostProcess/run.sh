#! /bin/sh

export OMP_NUM_THREADS=12
 
./src/run_analysis \
  -NUM_RANK				400		\
	-X_NUM_RANK			20		\
	-Y_NUM_RANK			20		\
	-X_RANK					480		\
	-Y_RANK					120		\
	-X_DOMAIN				9600	\
	-Y_DOMAIN				2400	\
	-Z_DOMAIN				500		\
	-dX							2.0		\
	-dT							0.008	\
	-FILE_START			1000	\
	-FILE_END				1190	\
	-POUT						125		\
	-PGEN_STEP			125		\
	-NUM_GEN				600		\
	-FLG_NUM				0			\
	-FLG_DENSITY		0			\
	-FLG_PROFILE		0			\
	-FLG_FOOT			 	0			\
	-FLG_FLUX				0			\
	-FLG_RESID			1			\
	-N_XY						3			\
	-Z_OUT					5 15 25 \
	-N_XZ						3			\
	-Y_OUT					1200 2400 3600\
	-N_YZ						3			\
	-X_OUT					11520 15360 19100\
	-H_AVE					10		\
	-N_SOURCE				30195 \
	-ID_DIGIT				4			\
	-N_SENSOR				3			\
	-CTR_SENSOR			18000.0	2400.0 	10.0 \
									18000.0	2400.0 	20.0 \
									18000.0	2400.0	30.0 \
	-SIZE_SENSOR		100.0 100.0 10.0 \
	-N_FLUX					1			\
	-Z_FLUX					10.0	\
	-Z_RESID				10.0 	\
	-DIR_DATA				../DATA_20210216_garuda/particle/	\
	-DIR_OUT				./Output_tmp	\
	-FNAME_MAP			./map/garuda_9600_2400_topo_fill		\
	-FNAME_SOURCE   ./particle_position/particle_position.txt \
	| tee	-a				./log_analysis.txt
