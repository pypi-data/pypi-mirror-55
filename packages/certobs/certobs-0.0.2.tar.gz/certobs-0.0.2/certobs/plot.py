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
from astropy.modeling import models, fitting

os.chdir(input("Directorio del archivo de potencias: "))

inp = str(input("Nombre del archivo .dat a leer: "))
f = open(inp, mode='r') #Archivo con tiempos y medidas de potencia
tiempo = np.genfromtxt(f, usecols = (0),delimiter=' ',dtype=("U15"))
f = open(inp, mode='r') #Archivo con tiempos y medidas de potencia
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
    #date = Time(hour, format='iso', scale='utc')

totalsec = totalsec * u.s
t0 = totalsec[0]
for i,row in enumerate(totalsec):
    totalsec[i] = totalsec[i] - t0

for i,tex in enumerate(pp):
    po.append(float(tex))
    

#TIPPING CURVE
plt.style.use('seaborn-talk')
plt.figure(figsize=(13,10))
plt.plot(totalsec,po,'.r')
plt.ylabel("Power meter (dBm)")
plt.xlabel("Time (s)")
plt.title(hour[0][:10]+"  " +inp[5:-4])
plt.savefig(hour[0][:10]+"  " +inp[5:-4])
plt.show()
