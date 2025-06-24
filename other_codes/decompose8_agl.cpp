#include<string>
#include<fstream>
#include<sstream>
#include<stdio.h>
#include<iostream>
#include<iomanip>	// setw, setfill

int sections=17;
//int imax=320,jmax=160,kmax=22,mmax=2;    //mmax: number of times
int nv0=0,nv1=9;  // select variables (all:0-15)
//int ncpu=80;
//int time0=187500;
int dtime=37500;
std::string fout_path ="BIN_dec";
//std::string input_csv_file_path  = "/mnt/f/LBM_TOKYO/RESTART_OUTPUT/D180S01/Output/";
std::string input_csv_file_path  = "/mnt/f/LBM_TOKYO/RESTART_OUTPUT/";


void ffname(int nv, std::string* variable){
	if(nv==0){*variable	= "xy_ag_um";}
	if(nv==1){*variable	= "xy_ag_vm";}
	if(nv==2){*variable	= "xy_ag_wm";}
	if(nv==3){*variable	= "xy_ag_uu";}
	if(nv==4){*variable	= "xy_ag_vv";}
	if(nv==5){*variable	= "xy_ag_ww";}
	if(nv==6){*variable	= "xy_ag_uv";}
	if(nv==7){*variable	= "xy_ag_uw";}
	if(nv==8){*variable	= "xy_ag_vw";}
	if(nv==9){*variable	= "xy_ag_gs";}
//	if(nv==9){*variable	= "xy_ag_uuu";}
//	if(nv==10){*variable= "xy_ag_vvv";}
//	if(nv==11){*variable= "xy_ag_www";}
//	if(nv==12){*variable= "xy_ag_ins_u";}
//	if(nv==13){*variable= "xy_ag_ins_v";}
//	if(nv==14){*variable= "xy_ag_ins_w";}
//	if(nv==15){*variable= "xy_ag_gs";}
}


void settings_for_sections(int section,int* ncpu,int* time0,int* imax,int* jmax,int* kmax,int* mmax){
	if(section==1){	*ncpu= 80;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==2){ *ncpu=240;*time0= 37500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==3){ *ncpu=240;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==4){ *ncpu=288;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==5){ *ncpu=304;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==6){ *ncpu=344;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==7){ *ncpu=376;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==8){ *ncpu=368;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==9){ *ncpu=352;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==10){*ncpu=400;*time0=187500;*imax=288;*jmax=160;*kmax=22,*mmax=2;}
	if(section==11){*ncpu=400;*time0=112500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==12){*ncpu=400;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==13){*ncpu=400;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==14){*ncpu=272;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==15){*ncpu=232;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==16){*ncpu=200;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
	if(section==17){*ncpu= 56;*time0=187500;*imax=320;*jmax=160;*kmax=22,*mmax=2;}
}

int main(){
	std::string variable;
	std::string str_buf;
	std::string str_conma_buf;
	std::ofstream fout;
//	int ijmax=imax*jmax;
	int ncpu,time0,imax,jmax,kmax,mmax;
	float *val;

	for(int section=1;section<sections+1;section++){
		settings_for_sections(section,&ncpu,&time0,&imax,&jmax,&kmax,&mmax);
		int ijmax=imax*jmax;

		for(int nv=nv0;nv<nv1+1;nv++){
			ffname(nv,&variable);
			for(int m=0; m<mmax; m++){
				int time=time0+m*dtime;
				for(int n=0; n<ncpu; n++){
					std::ostringstream fin_path;
					fin_path << input_csv_file_path 
						 << "D180S" << std::setw(2) << std::setfill('0') << section
						 << "/Output/"
						 << variable << std::setw(8) << std::setfill('0') << time << "_" 
						 << std::setw(4) << std::setfill('0') << n << ".csv";
					std::cout << fin_path.str() << std::endl;
					std::ifstream ifs_csv_file(fin_path.str());	//open input file
					int cnt=0,k=0;
					int ij;
					int kk;
					val=(float*)malloc(sizeof(float)*ijmax);
					while (getline(ifs_csv_file, str_buf)) {	//read input file
						if(cnt==0){
							cnt=cnt+1;
							continue;
						}	// header
						if(cnt==1){
							cnt=cnt+1;
							ij = 0;
							k=k+1;
							std::cout << str_buf << std::endl;
							kk=stoi(str_buf);
							continue;
						}	// header k
						std::istringstream i_stream(str_buf);
						while (getline(i_stream, str_conma_buf, ',')) {
							val[ij] = stof(str_conma_buf);
//							if(ij==ijmax-1){std::cout << ij << " " << val[ij] << std::endl;}
							ij=ij+1;
							//		ofs_csv_file << val << ',';
						}
//						std::cout << ij-1 << "-" << val[ij-1] << std::endl;
						if(ij==ijmax){
							cnt=1;
							std::ostringstream fout_name;
							fout_name << "./D180S" << std::setw(2) << std::setfill('0') << section
								  << "/"     << fout_path << "/" << variable
							  	  << std::setw(8) << std::setfill('0') << time	<< "_"
								  << std::setw(4) << std::setfill('0') << n	<< "_k"
								  << std::setw(4) << std::setfill('0') << kk	<< ".dat";
//							std::cout << fout_name.str() << std::endl;
							fout.open(fout_name.str(), std::ios::out|std::ios::binary|std::ios::trunc);
							if (!fout) {
								std::cout << "file not opened!" << std::endl;
								return 1;
							}
							fout.write(( char * ) val,sizeof(float)*ijmax );
//							std::cout<<"check " << val[1]<<std::endl;
							fout.close();
						}
					}	// ij loop
					ifs_csv_file.close();
					free(val);
				}	// n loop
			}	// m loop
		}	// nv loop
	}	// section loop
}	// main

