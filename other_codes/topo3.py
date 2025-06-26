import numpy as np
import pandas as pd
import gc

sections=1
xblock=1   # merge blocks in x
yblock=4   # merge blocks in y
list_ss=[ 9]
list_nx=[44]
list_ny=[ 4]

#nx=10
#ny=4
#nxy=nx*ny  # number of PEs total
#nxblock=4  # block average in x
#nyblock=8  # block average in y
dx=2.0     # grid resolution [m]
###xsub=320
###ysub=160
#casename='D180S01'
main_directory='../'
output_directory='./st_MAP/'
fname_bld='./map/building.dat'
fname_veg='./map/vegetation.dat'
fname_tpo='./map/topography.dat'
#fname_out='./MOUT/MAP_TILE_x'+str(nx).zfill(3)+'y'+str(ny).zfill(3)+'.csv'

def read_map(fname,nx,ny,xsub,ysub):
   p=pd.read_csv(fname,delim_whitespace=True,header=None,skiprows=1)
   p=np.array(p.T)
   print(p.shape)
   imax_map,jmax_map=p.shape
   if imax_map!=xsub*nx or jmax_map!=ysub*ny:
      print('*** ERROR ***')
      print('MAP[imax,jmax]=',imax_map,jmax_map)
      print('STA[imax,jmax]=',xsub*nx,ysub*ny)
      sys.exit()
   return p

def statistics(n,nx,ny,b,v,t):
   x,y=b.shape
   xy=x*y
   bave=0.0
   bstd=0.0
   bskw=0.0
   bkrt=0.0
   bmax=0.0
   bpa=0.0
   bfa=0.0
   bcnt=0
   vave=0.0
   vstd=0.0
   vskw=0.0
   vkrt=0.0
   vmax=0.0
   vpa=0.0
   vfa=0.0
   vcnt=0
   tave=0.0
   tstd=0.0
   tskw=0.0
   tkrt=0.0
   tmax=0.0
   tpa=0.0
   tfa=0.0
   tcnt=0
   for j in range(y):
      for i in range(x):
         if b[i,j]>0:
            bave=bave+b[i,j]
            bcnt=bcnt+1
            if b[i,j]>bmax:
               bmax=b[i,j]
            bpa=bpa+1.0
            if i>0 and b[i,j]-b[i-1,j]>0:
               bfa=bfa+(b[i,j]-b[i-1,j])
# vegetation
         if v[i,j]>0:
            vave=vave+v[i,j]
            vpa=vpa+1.0
            if v[i,j]>vmax:
               vmax=v[i,j]
            vcnt=vcnt+1
# topography
         tave=tave+t[i,j]
         if t[i,j]>tmax:
            tmax=t[i,j]

   if bcnt!=0:
      bave=bave/bcnt
      for j in range(y):
         for i in range(x):
            if b[i,j]>0:
               bd=b[i,j]-bave
               bstd=bstd+bd**2
               bskw=bskw+bd**3
               bkrt=bkrt+bd**4
      if bstd>0:
         bstd=(bstd/bcnt)**0.5
         bskw=(bskw/bcnt)/(bstd**3)
         bkrt=(bkrt/bcnt)/(bstd**4)
   bpa=bpa/xy
   bfa=bfa/xy
   if vcnt!=0:
      vave=vave/vcnt
      for j in range(y):
         for i in range(x):
            if v[i,j]>0:
               vd=v[i,j]-vave
               vstd=vstd+vd**2
               vskw=vskw+vd**3
               vkrt=vkrt+vd**4
      if vstd>0:
         vstd=(vstd/vcnt)**0.5
         vskw=(vskw/vcnt)/(vstd**3)
         vkrt=(vkrt/vcnt)/(vstd**4)
   vpa=vpa/xy
   tave=tave/xy
   for j in range(y):
      for i in range(x):
         td=t[i,j]-tave
         tstd=tstd+td**2
         tskw=tskw+td**3
         tkrt=tkrt+td**4
   if tstd>0:
      tstd=(tstd/xy)**0.5
      tskw=(tskw/xy)/(tstd**3)
      tkrt=(tkrt/xy)/(tstd**4)

   head=['n','nx','ny','bave','bstd','bskw','bkrt','bmax','bpa','bfa', \
                       'vave','vstd','vskw','vkrt','vmax','vpa',       \
                       'tave','tstd','tskw','tkrt','tmax' ]
   sta =[ n , nx , ny , bave , bstd , bskw , bkrt , bmax , bpa , bfa , \
                        vave , vstd , vskw , vkrt , vmax , vpa ,       \
                        tave , tstd , tskw , tkrt , tmax  ]
   return sta,head


def model_macdonald(ra,rf,h):
   if ra==0 or rf==0 or h==0:
      return 0,0
   a = 4.43
   b = 1.0
   c = 1.2
   k = 0.41   # Karman constant
   d = (1.0+a**(-ra)*(ra-1.0))*h
   z0= (1.0-d/h)*np.exp( -(0.5*b*c/(k**2.0)*(1.0-d/h)*rf))
   return z0,d


def model_kanda(ra,rf,h,hs,hmx,z0mac):     # h:average, hs:standard deviation
   if ra==0 or rf==0 or h==0:
      return 0,0
   a0= 1.29
   b0= 0.36
   c0= -0.17
   x = (hs+h)/hmx
   d = c0*x**2.0+(a0*ra**b0-c0)*x
   a1= 0.71
   b1= 20.21
   c1= -0.77
   y = ra*hs/h
   z0= (b1*y**2.0+c1*y+a1)*z0mac
   return z0,d


def output(st,head,fname_out):

   print('output  ',fname_out)
   header = pd.DataFrame(head).T
   header.to_csv(fname_out,index=False,header=False)
   df=pd.DataFrame(st)
   df.to_csv(fname_out,mode='a',header=False, index=False)
   df.to_csv(fname_out+'ESE',header=False, index=False)

def main():
   for s in range(sections):
      xsub=320
      ysub=320
      cname='D180S'+str(list_ss[s]).zfill(2)
#      print(cname)
      idir=main_directory

      nx=int(list_nx[s]/xblock)
      ny=int(list_ny[s]/yblock)
      nxy=nx*ny
      xsub=int(xsub*xblock)
      ysub=int(ysub*yblock)

      fname_out=output_directory+cname+'_x'+str(nx).zfill(3)+'y'+str(ny).zfill(3)+'.csv'

      b=np.zeros([xsub,ysub])
      t=np.zeros([xsub,ysub])
      v=np.zeros([xsub,ysub])
      bg=read_map(idir+fname_bld,nx,ny,xsub,ysub)
      tg=read_map(idir+fname_tpo,nx,ny,xsub,ysub)
      vg=read_map(idir+fname_veg,nx,ny,xsub,ysub)
      bst=[]

      for n2 in range(ny):
         for n1 in range(nx):
            n = n2*nx+n1
            i0=n1*xsub
            i1=i0+xsub
            j0=n2*ysub
            j1=j0+ysub
#            print(n,n1,n2,i0,i1,j0,j1)
            b=bg[i0:i1,j0:j1]
            t=tg[i0:i1,j0:j1]
            v=vg[i0:i1,j0:j1]
            b=b-t    # SUBTRACT TOPO FROM BUILD AND VEG
            v=v-t
            st,head=statistics(n,n1,n2,b,v,t)
            #[0:n,1nx,2ny,3ave,4std,5skw,6krt,7hmx,8hmi,9ra,10rf , h_tpo, h_veg, a_veg, tmax  ]

#            print(n1,n2,'st:',st)
#            print(type(st))
            z0m,dm=model_macdonald(st[8],st[9],st[3])    #ra,rf,h
            z0k,dk=model_kanda(st[8],st[9],st[3],st[4],st[7],z0m)   #ra,rf,h,hs,hmx,z0mac
            st.extend([z0m,dm,z0k,dk])
            head.extend(['z0m','dm','z0k','dk'])
#            print('st2',st)
#            bst=np.concatenate([bst,vmodels], 1)
#            print(bsta)
            bst.append(st)
      bst=np.array(bst)
      output(bst,head,fname_out)
#      print(bst)
      del bst
      del st
      gc.collect()


if __name__ == "__main__":
   main()

