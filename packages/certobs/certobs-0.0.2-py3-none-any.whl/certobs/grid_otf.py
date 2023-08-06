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
from astropy.time import Time, TimeDelta, TimezoneInfo
import os

os.chdir(input("Directorio del archivo de potencias: "))


f = open(input("Nombre del archivo .dat a leer: "), mode='r')   #Archivo con tiempos y medidas de potencia
tiempo = np.genfromtxt(f, usecols = (0),delimiter=' ',dtype=("U15"))
f = open(input("Nombre del archivo .dat a leer: "), mode='r')   #Archivo con tiempos y medidas de potencia
pp = np.genfromtxt(f, usecols = (1),delimiter=' ')

time = []
po = []
fecha = []
for i,tex in enumerate(tiempo):
    t = tex[9:]
    f = tex[:8]
    time.append(float(t))
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
for i,row in enumerate(time):
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
    date = Time(hour, format='iso', scale='utc')

t0 = totalsec[0]
for i,row in enumerate(totalsec):
    totalsec[i] = totalsec[i] - t0

for i,tex in enumerate(pp):
    po.append(float(tex))
    
#TIPPING CURVE
plt.style.use('seaborn')
plt.figure(figsize=(13,10))
plt.plot_date(date[295:460].plot_date,po[295:460],'r.')
plt.ylabel("Power meter (dBm)")
plt.xlabel("Time")
plt.title("Tipping curve 10-10-2019")
plt.show()

#TRANSIT
plt.style.use('seaborn')
plt.figure(figsize=(13,10))
plt.plot_date(date[1415:2005].plot_date,po[1415:2005],'g.')
plt.ylabel("Power meter (dBm)")
plt.xlabel("Time")
plt.title("Transit 10-10-2019")
plt.show()

#TRACKING
plt.style.use('seaborn')
plt.figure(figsize=(13,10))
plt.plot_date(date[2005:3067].plot_date,po[2005:3067],'b.')
plt.ylabel("Power meter (dBm)")
plt.xlabel("Time")
plt.title("Tracking 10-10-2019")
plt.show()

#SCANNING
plt.style.use('seaborn')
plt.figure(figsize=(13,10))
plt.plot_date(date[649:1368].plot_date,po[649:1368],'b.')
plt.ylabel("Power meter (dBm)")
plt.xlabel("Time")
plt.title("Scanning 10-10-2019")
plt.show()

###############################################################################
os.chdir("../obs2019-10-09")

data = open("datascan-2019.10.09-09.41.txt",mode='r')
datos=np.loadtxt(data,usecols=(1,2,3,4),skiprows=6)
data = open("datascan-2019.10.09-09.41.txt",mode='r')
tp =np.genfromtxt(data,usecols=(0),skip_header=6, dtype=(str))

tpp = []
for i,tex in enumerate(tp):
    tp = tex[11:]
    tpp.append(tp)
    
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

gridcoordsh = np.zeros((len(lra),len(ldec)),dtype=object)
gridpower = np.zeros((len(lra),len(ldec)))
gridn = np.zeros((len(lra),len(ldec)))
grid = np.zeros((len(lra),len(ldec)))

for i,row in enumerate(lra):
    for e,rew in enumerate(ldec):
        gridcoordsh[i][e] = (lra[i],ldec[e])
        for w in range(len(raint)):
            difra = abs(row - raint[w])
            difdec = abs(rew - decint[w])
            distance = np.sqrt(difra**2 + difdec**2)
            if distance < 0.62:
                gridpower[i][e] += po[w]
                gridn[i][e] += 1
        grid[i][e] = gridpower[i][e]/gridn[i][e]
        



##############################################################
fig = plt.figure(2,figsize=(12,12))
fig, ax = plt.subplots(constrained_layout=True,figsize=(12,10))

cmap2 = colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['black','blue','purple','red','orange','yellow'],
                                           256)

img2 = plt.imshow(grid,interpolation='nearest', cmap = cmap2,
                    origin='lower')

m = np.linspace(0,100,7)
mx = np.linspace(0,len(lra)-1,7)
perc = np.percentile(ra,m)
percy = np.percentile(dec,m)
perc = np.around(perc, decimals=1)
percy = np.around(percy, decimals=1)
labelx = [str(perc)]
#tickx = 

plt.xlabel('RA (degrees)')
plt.ylabel('DEC (degrees)')
plt.colorbar(img2,cmap=cmap2)

ax.tick_params(labeltop=True, labelright=True,bottom=True,top=True)

plt.xticks(mx,perc,rotation=45)
plt.yticks(mx,percy)








fig.savefig("image2.png")