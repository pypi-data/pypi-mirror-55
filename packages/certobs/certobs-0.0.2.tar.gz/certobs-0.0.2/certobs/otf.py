#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 10:45:37 2019

@author: dmoral
"""
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import astropy.units as u
from astropy.time import Time#, TimeDelta, TimezoneInfo
import os
import time
from astropy.io import fits
from pyds9 import DS9

os.chdir(input("Directorio del archivo de potencias: "))
inp = str(input("Nombre del archivo .dat a leer: "))

f = open(inp, mode='r')
tiempo = np.genfromtxt(f, usecols = (0),delimiter=' ',dtype=("U15"))
f = open(inp, mode='r')
pp = np.genfromtxt(f, usecols = (1),delimiter=' ')

timer = []
po = []
fecha = []
for i,tex in enumerate(tiempo):
    t = tex[9:]
    f = tex[:8]
    timer.append(float(t))
    fecha.append(int(f))
    
h = []
m = []
s = []
y = []
mo = []
d = []
hour = []
day = []
totalsec = []
for i,row in enumerate(timer):
    ho = int(str(row)[:-6])
    h.append(ho)
    mi = int(str(row)[-6:-4])
    m.append(mi)
    se = float(str(row)[-4:])
    s.append(se)
    sec = int(ho*3600 + mi*60 + se)
    totalsec.append(sec)
    
    ye = int(str(fecha[i])[:4])
    y.append(ye)
    mon = int(str(fecha[i])[4:6])
    mo.append(mon)
    da = int(str(fecha[i])[6:])
    d.append(da)
    day = '%s-%s-%s %s:%s:%s' %(ye,mon,da,ho,mi,se)
    hour.append(day)
    #date = Time(hour, format='iso', scale='utc') #Esto es lo que alarga el loop

t0 = totalsec[0]



for i,row in enumerate(totalsec):
    totalsec[i] = totalsec[i] - t0

for i,tex in enumerate(pp):
    po.append(float(tex))
    

    
###############################################################################
start = time.perf_counter()

co = str(input("Nombre del archivo de coordenadas a leer: "))

data = open(co,mode='r')
datos = np.loadtxt(data,usecols=(1,2,3,4),skiprows=6)
data = open(co,mode='r')
tp = np.genfromtxt(data,usecols=(0),skip_header=6, dtype=(str))

tpp = []
for i,tex in enumerate(tp):
    tpa = tex[11:]
    tpp.append(tpa)
    
hp = []
mp = []
sp = []
totalsecp = []

for i,row in enumerate(tpp):
    hop = int(str(row)[:-10])
    hp.append(hop)
    mip = int(str(row)[-9:-7])
    mp.append(mip)
    sep = float(str(row)[-6:])
    sp.append(sep)
    secp = int(hop*3600 + mip*60 + sep)
    totalsecp.append(secp)
    
tp0 = totalsecp[0]
for i,row in enumerate(totalsecp):
    totalsecp[i] = totalsecp[i] - tp0
    

ra = []
el = []
az = []
dec = []
for i,row in enumerate(datos):
    az.append(row[0])
    el.append(row[1])
    ra.append(row[2])
    dec.append(row[3])


azint = np.interp(totalsec,totalsecp,az)
elint = np.interp(totalsec,totalsecp,el)
raint = np.interp(totalsec,totalsecp,ra)
decint = np.interp(totalsec,totalsecp,dec)

    
ra0 = min(ra)
raf = max(ra)
dec0 = min(dec)
decf = max(dec)
paso = 1/12
lra = np.linspace(ra0,raf,((raf-ra0)*12)+1)
ldec = np.linspace(dec0,decf,((decf-dec0)*12)+1)

gridcoordsh = np.zeros((len(ldec),len(lra)),dtype=object)
gridpower = np.zeros((len(ldec),len(lra)))
gridn = np.zeros((len(ldec),len(lra)))
grid = np.zeros((len(ldec),len(lra)))


for i,row in enumerate(ldec):
    for e,rew in enumerate(lra):
        gridcoordsh[i][e] = (ldec[i],lra[e])
        for w in range(len(raint)):
            difra = abs(rew - raint[w])
            difdec = abs(row - decint[w])
            distance = np.sqrt(difra**2 + difdec**2)
            if distance < 0.62:
                gridpower[i][e] += po[w]
                gridn[i][e] += 1
        grid[i][e] = gridpower[i][e]/gridn[i][e]
       

end = time.perf_counter()
total = end - start
print("Tiempo total = "  + str(total))


#hdu = fits.BinTableHDU.from_columns(
 #       [fits.Column(name='RA', format='20A', array=totalsec),
  #       fits.Column(name='DEC', format='20A', array=totalsec),
   #      fits.Column(name='Power', format='E', array=po)])
#hay que darle una vuelta a esto para intentar exportar la grid entera
#hdr = fits.Header()
#hdr['SOURCE'] = 'Whatever'
#hdr['COMMENT'] = 'Lo que sea'
#primary_hdu = fits.PrimaryHDU(header=hdr)
#hdul = fits.HDUList([primary_hdu, hdu])
#hdul.writeto('tabla.fits')

###############################################################################

fig, ax = plt.subplots(constrained_layout=True,figsize=(8,6))

cmap2 = colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['black','blue','purple','red','orange','yellow','green'],
                                           256)
cmap3 = colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['black','blue','purple','red'],
                                           256)

img2 = plt.imshow(grid,interpolation='nearest', cmap = "plasma", origin='lower')
#cmap2 en vez de "plasma"
#img3 = plt.imshow(grid,interpolation='spline16', cmap = cmap3, origin='lower')

m = np.linspace(0,100,7)
mx = np.linspace(0,len(lra)-1,7)
my = np.linspace(0,len(ldec)-1,7)
percx = np.percentile(ra,m)
percy = np.percentile(dec,m)
percx = np.around(percx, decimals=1)
percy = np.around(percy, decimals=1)
#tickx = 

plt.xlabel('RA (degrees)',va="top")
plt.ylabel('DEC (degrees)')
plt.title('Scanning '+hour[0][:10]+" " +inp[5:-4])
plt.colorbar(img2,cmap=cmap2)
#plt.colorbar(img3,cmap=cmap3)

ax.tick_params(labeltop=True, labelright=True,bottom=True,top=True)

plt.xticks(mx,percx,rotation=45)
plt.yticks(my,percy)


plt.savefig('scan'+hour[0][:10]+"_" +inp[5:-4])

datos = fits.open('scan2019-10-30.fits')

hdu1 = fits.PrimaryHDU()
hdu2 = fits.ImageHDU(data=datos[0].data)

hdu.header['TYPE'] = 'Scanning'
hdu.header['NSIDE'] = 256
hdu.header['ORDERING'] = 'NESTED'
hdu.header['COORDSYS'] = 'ICRS'

hdul = fits.HDUList([hdu1, hdu2])
hdul.writeto('scan'+hour[0][:10]+'.fits', overwrite=True)
hdul[1].name = 'POWER-MAP'

DS9('scan'+hour[0][:10]+'.fits')