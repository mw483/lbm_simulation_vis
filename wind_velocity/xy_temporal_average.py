import numpy as np
sections=1               # number of independent sections
d_in    ='./BIN_dec/'     # input directly
d_out   ='./BIN_dec_av/'  # output directory
dtime   =37500            # time increment
nsteps  =2                # number of timesteps to integrate
nvariables=12             # number of variables
nlevels =22               # number of height

## file name     BIN_dec/xy_ag_um00187500_0000_k0002.dat

def main():
   # variable loop
   for var in range(nvariables):
      vname=variables(var)

      # section loop
      for s0 in range(sections):
         imax_s,jmax_s,nx,ny,nmax,imax,jmax,ijmax,time0=section_parameters(s0)
         d_section='./D180S'+str(s0+1).zfill(2)+'/'
         print(d_section)

         # ncpu loop
         for n in range(nmax):
            print(d_section+d_in+vname+' n:'+str(n).zfill(3)+'/'+str(nmax).zfill(3))
            # height loop
            for k0 in range(nlevels):
#               print(d_section+d_in+vname)
               k=levels(k0)
               cnt=0

               # time integration and average
               for nt in range(nsteps):
                  time=time0+dtime*nt
                  fname=filename(vname,time,n,k)
#                  print(fname)
                  if nt==0:
                     array_output=input_data(d_section+d_in,fname)
                     cnt=cnt+1
                  else:
                     array=input_data(d_section+d_in,fname)
                     array_output=array_output+array
                     cnt=cnt+1
               array_output=array_output*0.5

               # output
               output_data(array_output,d_section+d_out,fname) 

   exit()



def section_parameters(s):
   imax_table=[320]
   jmax_table=[160]
   nx_table  =[ 44]
   ny_table  =[  8]
   time_table=[187500]
   imax_s=imax_table[s]
   jmax_s=jmax_table[s]
   nx=nx_table[s]
   ny=ny_table[s]
   nmax=nx*ny
   imax=imax_s*nx
   jmax=jmax_s*ny
   ijmax=imax*jmax
   time=time_table[s]
   return imax_s,jmax_s,nx,ny,nmax,imax,jmax,ijmax,time



def variables(var):
#          0    1    2    3    4    5    6    7    8    9       10      11
   vnames=['um','vm','wm','uu','vv','ww','uw','vw','gs','ins_u','ins_v','ins_w']
   return 'xy_ag_'+vnames[var]


def levels(k):
   level=[1,2,3,4,8,12,16,20,24,28,32,40,48,64,74,75,76,100,150,200,250,300]
   return level[k]


def filename(vname,time,n,k):
## (ex) xy_ag_um00187500_0000_k0002.dat
   fname=vname+str(time).zfill(8)+'_'+str(n).zfill(4)+'_k'+str(k).zfill(4)
   return fname

def input_data(fpath,fname):
#   print(fpath+fname+'.dat')
   array=np.fromfile(fpath+fname+'.dat',dtype='float32')
   return array


def output_data(array,fpath,fname):
   array=array.tofile(fpath+fname+'.dat')



if __name__ == '__main__':
   main()
