#####
#   Run "topo.py before this process
#####

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize as op
from matplotlib.collections import LineCollection


list_ss=[ 9]
list_nx=[44]
list_ny=[ 4]

dirgeo='./st_MAP/'


#nx=44      # number of total PEs in x
#ny=8       # number of total PEs in y
#nxy=nx*ny  # number of PEs total
nxblock=1  # block average in x
nyblock=4  # block average in y 

dx=2.0     # grid resolution [m]

tave=11     # average steps (averaging time)
timetable=[375000,390000,405000,420000,435000,450000,465000,480000,495000,510000,525000]
#timetable=[37500,75000,112500,150000,187500,225000,262500,300000,337500,375000,412500,450000,487500]
#timetable=[ 19000, 37500, 56500, 75000, 94000,112500,
#           131500,150000,169000,187500,206500,225000,
#           244000,262500,281500,300000,319000,337500,
#           356500,375000,394000,412500,431500,450000,
#           469000,487500,506500,525000,544000,562500,
#           581500,600000,619000,637500,656500,675000,
#           694000,712500,731500,750000,769000]
tmax=len(timetable)
#list_t0=[37500,37500,37500,37500,37500,37500,37500,37500,37500,37500,37500,37500,37500,37500,37500,37500,37500]
#list_t0=[225000,75000,225000,225000,225000,225000,225000,37500,225000,225000,
#         150000,150000,225000,225000,225000,225000,225000]
#t0  =225000
dt  =37500
# input
fname='prof'
idir='../Output/'
#fname_geo='./P1/MAP_TILE_'
# output
odir='./st_PROF_1ET/'
odir_aero='./st_PROF_1ET/'
odirfig='./FIG/'
def read_geofile(nx,ny,section,dr):
   x=int(nx/nxblock)
   y=int(ny/nyblock)
   fin='D180S'+str(section).zfill(2)+'_x'+str(x).zfill(3)+'y'+str(y).zfill(3)+'.csv'
   print(dr+fin)
   pp=pd.read_csv(dr+fin,skiprows=1,header=None)
#   p=np.array(pp)
   stgeo=np.array(pp)
#   print(pb)
#  [0n ,1nx ,2ny ,3bave ,4bstd ,5bskw ,6bkrt ,7bmax ,8bpa ,9bfa , \
#                10vave,11vstd,12vskw,13vkrt,14vmax,15vpa ,       \
#                16tave,17tstd,18tskw,19tkrt,20tmax  ]
   h,w=stgeo.shape
   print('stgeo:',h,w)
#   if nxy!=h:
#   print(nx,h)
#      print(p)
#      print("error")
#   stgeo=average_in_block_geo(p)
#   ave=pb[:,3]
#   std=pb[:,4]
#   skw=pb[:,5]
#   krt=pb[:,6]
#   hmx=pb[:,7]
#   hmi=0.0
#   ra =pb[:,8]
#   rf =pb[:,9]
#   ztp=pb[:,16]
#   zvg=pb[:,10]
#   avg=pb[:,15]
#   tmx=pb[:,20]
#   return ave,std,skw,krt,hmx,ra,rf,ztp,zvg,avg,tmx
   return stgeo

def sort_stgeo(stgeo):
#  [0n ,1nx ,2ny ,3bave ,4bstd ,5bskw ,6bkrt ,7bmax ,8bpa ,9bfa , \
#                10vave,11vstd,12vskw,13vkrt,14vmax,15vpa ,       \
#                16tave,17tstd,18tskw,19tkrt,20tmax,              \
#   21z0m,22dm,23z0k 24dk  ]
   print(stgeo.shape)
   bav=stgeo[:,3]
   bst=stgeo[:,4]
   bmx=stgeo[:,7]
   ra =stgeo[:,8]
   rf =stgeo[:,9]
   tav=stgeo[:,16]
   tmx=stgeo[:,20]
   return bav,bst,bmx,ra,rf,tav,tmx

def average_in_block_geo(p):
   nxb = int(nx/nxblock)
   nyb = int(ny/nyblock)
   nxy=nxb*nyb
   n0,n1=p.shape
   pb=np.zeros([nxy,n1])
   print('AAA',pb.shape)
   for xb in range(nxb):
      for yb in range(nyb):
         idb = yb*nxb + xb
         for x in range(nxblock):
            for y in range(nyblock):
               idx = xb*nxblock + x
               idy = yb*nyblock + y
               id  = idy*nx + idx
#               print(nxb,nyb,idx,idy,id,idb)
               pb[idb,:]=pb[idb,:]+p[id,:]
         pb[idb,:]=pb[idb,:]/(nxblock*nyblock)
   return pb


def read_prof(dr,n,time):
   ierr=0
   path = dr+idir+fname+str(time).zfill(8)+'_'+str(n).zfill(4)+'.csv'
   print(path)
   is_file = os.path.isfile(path)
   if is_file:
      pp=pd.read_csv(dr+idir+fname+str(time).zfill(8)+'_'+str(n).zfill(4)+'.csv',skiprows=1)
      p=np.array(pp)
      p=p.T            # p[variable,heihgt]
   else:
      ierr=1
      p=np.zeros((5,5))
   return p,ierr


def sum_variables(p,pa):
   pa = pa + p
   return pa


def output(s,pa,time):   #(s,n,pa)
#   pyout=np.stack([xx[0,:],pyave,pystd,pymax,pymin])
#   header=['z[m]','ave','std','max','min']
   header=['z' ,'RHO','U' ,'V' ,'W'  ,'UU' ,'VV' ,'WW' ,'UV' ,'UW',
           'VW','RU' ,'RV','RW','UUU','VVV','WWW','UUW','VVW','T' ,
           'TT','UT' ,'VT','WT','TTT']
   nval=len(header)
   for nv in range(nval):
      vout=pa[:,nv,:] 
      vout_pd=pd.DataFrame(vout.T)
      vout_pd.to_csv(odir+header[nv]+str(s).zfill(2)+'t'+str(time).zfill(8)+'.csv',index=False)
   return


def drawlines(s,time,pz,aero,stgeo):
   header=['z' ,'RHO','U' ,'V' ,'W'  ,'UU' ,'VV' ,'WW' ,'UV' ,'UW',
           'VW','RU' ,'RV','RW','UUU','VVV','WWW','UUW','VVW','T' ,
           'TT','UT' ,'VT','WT','TTT']
   print('pz:',pz.shape)
   aero=np.array(aero)
   print('aero:',aero.shape)
   nxy,nv,kmax=pz.shape
   n0 =stgeo[:,1]  # nx
   n1 =stgeo[:,2]  # ny
   blh= aero[:,3]
   uf = aero[:,2]
   ust= aero[:,4]
   bav=stgeo[:,3]
   tav=stgeo[:,16]

   cmap = plt.get_cmap('rainbow')

   z  =np.zeros((kmax))
   val=np.zeros((kmax))
   var=2

# Draw
   fig=plt.figure()
   ax = fig.add_subplot(1, 1, 1)
   for n in range(nxy):
#      if n0[n]<8:
#         continue
      for k in range(kmax):
         z[k]=(k*dx-tav[n])  #/blh[n]
         val[k]=pz[n,var,k]/(uf[n]**1)
      ind=n0[n]/40
      ax.plot(val,z,linewidth=0.75,color=cmap(ind))
      ax.set_ylim(0,600)
      ax.set_xlim(0,1)
#   plt.show()
   plt.savefig(odirfig+header[var]+'_D180S'+str(s).zfill(2)+'t'+str(time).zfill(8)+'.png')
   plt.clf()
   plt.close()

   return

def calculate_moment(pa):
#   pa[nxy,var,z]
   x,y,z=pa.shape
   print(x,y,z)
   for n in range(x):
      for k in range(z):
         pa[n,5,k]  = pa[n,5,k]  - pa[n,2,k]*pa[n,2,k]  # uu
         pa[n,6,k]  = pa[n,6,k]  - pa[n,3,k]*pa[n,3,k]  # vv
         pa[n,7,k]  = pa[n,7,k]  - pa[n,4,k]*pa[n,4,k]  # ww
         pa[n,8,k]  = pa[n,8,k]  - pa[n,2,k]*pa[n,3,k]  # uv
         pa[n,9,k]  = pa[n,9,k]  - pa[n,2,k]*pa[n,4,k]  # uw
         pa[n,10,k] = pa[n,10,k] - pa[n,3,k]*pa[n,4,k]  # vw
   return pa


def average_in_block(pa):
   nxb = int(nx/nxblock)
   nyb = int(ny/nyblock)
   nxy=nxb*nyb
   x,y,z=pa.shape
#   print(x,y,z)
   pb=np.zeros([nxy,y,z])
   n0=np.zeros([nxy])
   n1=np.zeros([nxy])
   for xb in range(nxb):
      for yb in range(nyb):
         idb = yb*nxb + xb
         n0[idb]=xb
         n1[idb]=yb
         for x in range(nxblock):
            for y in range(nyblock):
               idx = xb*nxblock + x
               idy = yb*nyblock + y
               id  = idy*nx + idx
#               print(nxb,nyb,idx,idy,id,idb)
               pb[idb,:,:]=pb[idb,:,:]+pa[id,:,:]
         pb[idb,:,:]=pb[idb,:,:]/(nxblock*nyblock)
   return n0,n1,pb


def boundary_layer_height_uf(um,tav):
   z=len(um)
   umax=0.0
   for k in range(10,z-10):
      if um[k]>umax:
         umax=um[k]
   for k in range(10,z-10):
      if um[k]>0.99*umax:
         blh=k*dx-tav
         break
   return umax,blh


def friction_velocity(uw):
   z=len(uw)
   uwmax=0.0
   zpuw=0.0
   for k in range(10,z-10):
      if -uw[k]>uwmax:
         uwmax=-uw[k]
         zpuw=k*dx
   return uwmax**0.5,zpuw

def friction_velocity_interpolation(uw,zb,zt,tav):
   z=len(uw)
   kmin=int(zb/dx)
   kmax=int(zt/dx)
   if kmax-kmin<2:
      kmax=kmin+2
   n=0
   xdata=np.zeros([kmax-kmin])
   ydata=np.zeros([kmax-kmin])
   for k in range(kmin,kmax):
      xdata[n]=(k+0.5)*dx-tav
      ydata[n]=uw[k]
      n=n+1
   parameter0=[0.,0.]
   result = op.leastsq(fit_func,parameter0,args=(xdata,ydata))
   a_fit=result[0][0]
   b_fit=result[0][1]
#   print(result)
   ustar=abs(b_fit)**0.5
   return ustar,a_fit

def fit_func(parameter,x,y):
    a = parameter[0]
    b = parameter[1]
    residual = y-(a*x+b)
    return residual


def fitting_range(bav,tav,blh,f1,f2):
   zb=bav*f1+tav
   zt=blh*f2+tav
   if zt<zb:
      zt=bav*(f1+1.0) + tav
   return zb,zt


def log_law(um,ustar,tav,zb,zt):
   kmax=len(um)
   k0=int(zb/dx)
   k1=int(zt/dx)
   if k1-k0<3:
      k1=k0+3
   x=np.zeros([k1-k0])
   y=np.zeros([k1-k0])
   kk=0
   for k in range(k0,k1):
      y[kk]=um[k]/ustar
      x[kk]=k*dx-tav
      kk=kk+1
   x=np.array(x)
   y=np.array(y)
#   print(x)
#   print(y)
   parameter0=[0.1,1.0]
   result = op.leastsq(loglaw_func,parameter0,args=(x,y))
   z0=result[0][0]
   d =result[0][1]
   return z0,d


def loglaw_func(parameter,x,y):
   z0 = parameter[0]
   d  = parameter[1]
   residual = y-2.5*np.log((x-d)/z0)
   return residual


def aerodynamic_parameters(n0,n1,pa,bav,tav):
   x,y,z=pa.shape         # x:nxy, y:var, z:height
   px=np.zeros([x,5,z])   # 0:Uf, 1:blh, 2:u*, 3:z0, 4:d
   paero=[]
   for n in range(x):
      um=pa[n,2,:]  # mean u
      uw=pa[n,9,:]  # u'w'
      uf,blh        = boundary_layer_height_uf(um,tav[n])
      zb,zt         = fitting_range(bav[n],tav[n],blh,2.0,0.2)
      ustar,zpuw    = friction_velocity(uw)
      ustar2,duw_dz = friction_velocity_interpolation(uw,zb,zt,tav[n])
      z0,d          = log_law(um,ustar,tav[n],zb,zt)
#      print(uf,blh,ustar,ustar2,zb,zt)
      paero.append([n0[n],n1[n],uf,blh,ustar,ustar2,zb,zt,z0,d,duw_dz,zpuw])
   return paero

def output_aero(s,time,aero):
   aero=np.array(aero)
   aero_pd=pd.DataFrame(aero)
   aero_pd.to_csv(odir_aero+'aero'+str(s).zfill(2)+'t'+str(time).zfill(8)+'.csv',index=False,header=False)


def diagnostic_plot(s,p,aero,tave,nx,ny):
#   print('p:',p.shape)
#   print('aero:',np.array(aero).shape)
#   print('tave:',tave.shape)
   nxy,var,kmax=p.shape
   um=p[:,2,:]
   uu=p[:,5,:]
   uf=np.array(aero)[:,2]
#   print('um:',um.shape)
   dplt=np.zeros((nxy,2,kmax))
   for n in range(nxy):
      for k in range(kmax):
         if um[n,k]>0:
            dplt[n,0,k]=um[n,k]/uf[n]
            if uu[n,k]>0:
               dplt[n,1,k]=((uu[n,k])**0.5)/um[n,k]
            else:
               dplt[n,1,k]=0.0
# output diagnostic plot variables
      dplt_pd=pd.DataFrame(dplt[:,0,:].T)
      dplt_pd.to_csv(odir+'DPL_UMUF'+str(s).zfill(2)+'.csv',index=False)
      dplt_pd=pd.DataFrame(dplt[:,1,:].T)
      dplt_pd.to_csv(odir+'DPL_UUUM'+str(s).zfill(2)+'.csv',index=False)
# find fitting height
   al=np.zeros(nxy)
   bl=np.zeros(nxy)
   rl=np.zeros(nxy)
   au=np.zeros(nxy)
   bu=np.zeros(nxy)
   ru=np.zeros(nxy)
   xc=np.zeros(nxy)
   yc=np.zeros(nxy)
   zstar=np.zeros(nxy)
   for n in range(nxy):
      for k in range(3,kmax):
         if dplt[n,0,k]>0.22:
            kl0=k
            break
      for k in range(kl0,kmax):
         if dplt[n,0,k]>0.4:
            kl1=k
            break
      for k in range(kl1,kmax):
         if dplt[n,0,k]>0.6:
            ku0=k
            break
      for k in range(ku0,kmax):
         if dplt[n,0,k]>0.8:
            ku1=k
            break
      print(kl0,kl1,ku0,ku1)
      al[n],bl[n],rl[n]=least_sq(dplt[n,0,kl0:kl1],dplt[n,1,kl0:kl1])   # slope,intercept,R2=least_sq(X,Y)
      au[n],bu[n],ru[n]=least_sq(dplt[n,0,ku0:ku1],dplt[n,1,ku0:ku1])   # slope,intercept,R2=least_sq(X,Y)
      if rl[n]==0 or ru[n]==0:
         xc[n]=-1.0
         yc[n]=-1.0
      else:
         xc[n],yc[n]=intercept(al[n],bl[n],au[n],bu[n])
      print('xc,yc:',xc,yc,al[n],bl[n],au[n],bu[n])
#      print('x,y:',x,y,al,bl,au,bu)
      zstar[n]=umuf_to_z(xc[n],dplt[n,0,:],tav[n])
      print('zstar:',zstar[n])

# plot
   fig=plt.figure()
   cmap = plt.get_cmap('rainbow')
   ax = fig.add_subplot(1, 1, 1)
   for n in range(nxy):
#      if n0[n]<8:
#         continue
      for k in range(kmax):
         x=dplt[n,0,:]
         y=dplt[n,1,:]
      ind=nx[n]/40
      ax.plot(x,y,linewidth=0.75,color=cmap(ind))  # plot lines
      ax.plot(xc,yc,linewidth=0,marker="o",markersize=5,markerfacecolor='black',markeredgecolor='black')
      plt.xlim(0,1.2)
      plt.ylim(0,1.0)
#   plt.show()
   plt.savefig(odirfig+'DP_D180S'+str(s).zfill(2)+'.png')
   plt.clf()
   plt.close()
   return zstar


def umuf_to_z(x,umuf,ztopo):
   if x<0:
      zstar=0.0
      return zstar
   kmax=len(umuf)
   for k in range(2,kmax):
#      print(n,x,umuf[k])
      if x<umuf[k]:
         zstar=k*dx-ztopo
         break
      zstar=0.0
   return zstar


def intercept(a0,b0,a1,b1):
   x=-(b0-b1)/(a0-a1)
   y=a0*x+b0
   return x,y


def least_sq(x,y):
   nmax=len(x)
   if nmax<2:
      return 0,0,0
#   print('nmax:',nmax)
   xm=0.0
   ym=0.0
   xx=0.0
   yy=0.0
   xy=0.0
   for n in range(nmax):
      xm=xm+x[n]
      ym=ym+y[n]
      xx=xx+x[n]*x[n]
      yy=yy+y[n]*y[n]
      xy=xy+x[n]*y[n]
   slope    =(nmax*xy-xm*ym)/(nmax*xx-xm*xm)
   intercept=(xx*ym-xy*xm)  /(nmax*xx-xm*xm)
   dy2 =0.0
   dy2m=0.0
   for n in range(nmax):
      dy2 =dy2 +(y[n]-ym/nmax)**2
      dy2m=dy2m+(y[n]-(slope*x[n]+intercept))**2
   r2=1.0-dy2m/dy2
   return slope,intercept,r2

def output_aero_geo(s,time,aero,stgeo,zstar):
   aero_np=np.array(aero)
   zstar_np=np.array(zstar)
#   print('aero :',aero_np.shape)
#   print('stgeo:',stgeo.shape)
#   geo=np.c_[bav,bst,bsk,bkr,bmx,ra,rf,tav,vav,vaa]
   print(stgeo.shape,aero_np.shape,zstar_np.shape)
   allval=np.hstack((stgeo,aero))
   allval=np.c_[allval,zstar_np]
#   head=['bav','bst','bsk','bkr','bmx','ra','rf','tav','vav','vaa',
#         'nx','ny','uf','blh','ust1','ust2','zb','zt','z0','d','duw_dz','zpuw']
   head=['n','nx','ny',                                    \
         'bave','bstd','bskw','bkrt','bmax','bpa','bfa',   \
         'vave','vstd','vskw','vkrt','vmax','vpa',         \
         'tave','tstd','tskw','tkrt','tmax',               \
         'z0m','dm','z0k','dk',
         'nx','ny','uf','blh','ust1','ust2','zb','zt','z0','d','duw_dz','zpuw',  \
         'zstar']
   head_np=np.array(head)
   head_pd=pd.DataFrame(head_np).T
   head_pd.to_csv(odir_aero+'geo_aero'+str(s).zfill(2)+'t'+str(time).zfill(8)+'.csv',index=False,header=False)
   allval_pd=pd.DataFrame(allval)
   allval_pd.to_csv(odir_aero+'geo_aero'+str(s).zfill(2)+'t'+str(time).zfill(8)+'.csv',mode='a',index=False,header=False)
   allval_pd.to_csv(odir_aero+'geo_aero'+str(s).zfill(2)+'t'+str(time).zfill(8)+'.csv.ESE',index=False,header=False)

#=== stgeo
#  [0n ,1nx ,2ny ,3bave ,4bstd ,5bskw ,6bkrt ,7bmax ,8bpa ,9bfa , \
#                10vave,11vstd,12vskw,13vkrt,14vmax,15vpa ,       \
#                16tave,17tstd,18tskw,19tkrt,20tmax,              \
#   21z0m,22dm,23z0k 24dk  ]
#=== aero
#  'nx','ny','uf','blh','ust1','ust2','zb','zt','z0','d','duw_dz','zpuw'


def check_variables(pb,stgeo):
   print('pb   :',pb.shape)
   print('stgeo:',stgeo.shape)
   return

###### driver ######

sections=1

for s0 in range(sections):

   nx=list_nx[s0]   # npcu x
   ny=list_ny[s0]   # ncpu y
#   t0=list_t0[s0]   # timestep
   nxy=nx*ny

   s=list_ss[s0]
   dirsec='./'
#   dirgeo='./MOUT/'

#   bav,bst,bsk,bkr,bmx,ra,rf,tav,vav,vaa,tmx=read_geofile(nx,ny,s,dirgeo)

   stgeo=read_geofile(nx,ny,s,dirgeo)
   bav,bst,bmx,ra,rf,tav,tmx=sort_stgeo(stgeo)
#   print("stgeo",stgeo)

   cnt=0
   for t in range(tmax):
      time=timetable[t]
      for n in range(nxy):    # nxy before block avearage
         p,ierr=read_prof(dirsec,n,time)   # read all profiles
         if ierr==1:
            print('no file! : '+dirsec+str(n)+"  "+str(time))
            break
         if t==0 and n==0:
            h,w=p.shape
            pa=np.zeros([nxy,h,w])
         pa[n,:,:]=pa[n,:,:]+p[:,:]
#      print("pa",pa)
############################################   Error associated with time increment

      if ierr==1:
         break

      cnt+=1
      if (t+1)%tave==0:      # averaging and output process
         pa/=tave
         n0,n1,pb = average_in_block(pa)       # block average  pa->pb
         pa[:,:,:]=0.0   # initialize pa
         check_variables(pb,stgeo)
#      print(pb[:,2,300])
#      exit()
         pz       = calculate_moment(pb)       # calculate statistical moment
#      print(pz[:,2,300])
#      exit()
         aero     = aerodynamic_parameters(n0,n1,pz,bav,tav)            # calculate integrated variables
#         output_aero(s,time,aero)
#         output_aero_geo(s,time,aero,stgeo)
#      print(pz[:,2,300])
#      exit()
         zstar=diagnostic_plot(s,pz,aero,tav,stgeo[:,1],stgeo[:,2])
         output_aero_geo(s,time,aero,stgeo,zstar)

         output(s,pz,time)                      # output csv
         drawlines(s,time,pz,aero,stgeo)
         cnt=0


