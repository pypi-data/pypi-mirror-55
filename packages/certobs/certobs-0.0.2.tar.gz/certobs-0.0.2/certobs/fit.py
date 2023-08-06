#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:09:41 2019

@author: dmoral
"""

from astropy.modeling import models, fitting
from matplotlib import pyplot as plt
import numpy as np
import astropy.units as u
import os
from glob import glob
from scipy import stats


pars = []
def fit(power_file, model):
    d = input("Directorio del archivo de potencias: ")
    os.chdir(d)
    vals = list()
#    vall = []
#gl= glob('power*')
#for a in gl:
    inp = str(power_file)
    
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
    
    for i,r in enumerate(po):
        po[i] -= min(po)
    
    #Selección de intervalos
    print("Seleccione el intervalo de medidas útil para el ajuste.")
    c0def = 0
    p0 = input("Primer punto útil (enter para el primero): ")
    if not p0:
        p0 = c0def
    c0 = int(p0)
    
    cfdef = ':'
    pf = input("Último punto útil (enter para último, -1 para el penúltimo): ")
    if not pf:
        cf = cfdef
    else: cf = int(pf)
    
    po = po[c0:print(cf)]
    totalsec = totalsec[c0:print(cf)]
    
    if model=='Mexican' or model=='Mexi' or model=='mexi' or model=='mexico' or model=='mex' or model=='mexican' or model=='Mexico':
        modelg = models.MexicanHat1D(amplitude=1, x_0=400, sigma=100)
        fitter = fitting.LevMarLSQFitter()
        ajusteg = fitter(modelg, totalsec, po)
        
        #modell = models.Lorentz1D(amplitude=0.5, x_0=300, fwhm=100)
        #fitter = fitting.LevMarLSQFitter()
        #ajustel = fitter(modell, totalsec, po)
        #if fitter.fit_info['message'] == 
        
        tope = 1.2 * max(po[150:-150])
        
        vals.append((str(inp[6:-4]),ajusteg.amplitude.value,ajusteg.x_0.value, ajusteg.sigma.value))
        #vall.append((str(inp[6:-4]),ajustel.amplitude.value,ajustel.x_0.value, ajustel.fwhm.value))
    
        plt.figure(figsize=(13,10))
        plt.plot(totalsec.value, po, 'r.', label="Datos",linewidth=1,ms=4)
        plt.plot(totalsec.value, ajusteg(totalsec), 'b',label="Mexican Hat",linewidth=1,ms=4)
        #plt.plot(totalsec.value, ajustel(totalsec), 'g',label="Lorentziana",linewidth=1,ms=4)
        plt.ylim(0,tope)
        plt.xlim(0,600)
        plt.ylabel(r'Power (dBm)')
        plt.xlabel('Tiempo (s)')
        plt.title('Mexican '+hour[0][:10]+"  " +inp[6:-4])
        
        a = np.around(ajusteg.amplitude.value,decimals=2)
        b = np.around(ajusteg.x_0.value,decimals=2)
        c = np.around(ajusteg.sigma.value,decimals=2)
        chi = np.around(stats.chisquare(po,ajusteg(totalsec)).statistic,decimals=2)
        #if c > 150 or chi =='nan' or chi>40000:
        #    a,b,c,chi = '----'
    
        plt.legend(title = "Ajuste:")
        texto = ("Amplitude = "+str(a)+"\nx_0 = "+str(b)+"\nSigma = "
                 +str(c)+"\nChi² = "+str(chi))
        pars.append((inp[6:-4],a,b,c,chi))
        medio = 6*tope/8
        plt.text(520, medio, texto, size=13, ha="center", va="center")
            
        directorio = './Ajustes'
        
        try:
            os.stat(directorio)
        except:
            os.mkdir(directorio)
            
        os.chdir(directorio)
        plt.savefig("MexicanHat "+hour[0][:9]+"_" +inp[13:-4])
        plt.show()
    
    elif model=='Gauss' or model=='Gaussian' or model=='Normal' or model=='gauss' or model=='gaussian' or model=='normal':
        modelg = models.Gaussian1D(amplitude=0.5, mean=300, stddev=120)
        fitter = fitting.LevMarLSQFitter()
        ajusteg = fitter(modelg, totalsec, po)
        
        #modell = models.Lorentz1D(amplitude=0.5, x_0=300, fwhm=100)
        #fitter = fitting.LevMarLSQFitter()
        #ajustel = fitter(modell, totalsec, po)
        #if fitter.fit_info['message'] == 
        
        tope = 1.2 * max(po[150:-150])
        
        vals.append((str(inp[6:-4]),ajusteg.amplitude.value,ajusteg.mean.value, ajusteg.stddev.value))
        #vall.append((str(inp[6:-4]),ajustel.amplitude.value,ajustel.x_0.value, ajustel.fwhm.value))
    
        plt.figure(figsize=(13,10))
        plt.plot(totalsec.value, po, 'r.', label="Datos",linewidth=1,ms=4)
        plt.plot(totalsec.value, ajusteg(totalsec), 'b',label="Gaussiana",linewidth=1,ms=4)
        #plt.plot(totalsec.value, ajustel(totalsec), 'g',label="Lorentziana",linewidth=1,ms=4)
        plt.ylim(0,tope)
        plt.xlim(0,600)
        plt.ylabel(r'Power (dBm)')
        plt.xlabel('Tiempo (s)')
        plt.title('Gaussian '+hour[0][:10]+"  " +inp[6:-4])
        
        a = np.around(ajusteg.amplitude.value,decimals=2)
        b = np.around(ajusteg.mean.value,decimals=2)
        c = np.around(ajusteg.stddev.value,decimals=2)
        chi = np.around(stats.chisquare(po,ajusteg(totalsec)).statistic,decimals=2)
            
        if c > 150 or chi =='nan' or chi>40000:
            a,b,c,chi = '----'
        
        plt.legend(title = "Ajuste:")
        texto = ("Amplitude = "+str(a)+"\nMean = "+str(b)+"\nStdDev = "
                 +str(c)+"\nChi² = "+str(chi))
        pars.append((inp[6:-4],a,b,c,chi))
        medio = 6*tope/8
        plt.text(520, medio, texto, size=13, ha="center", va="center")
            
        directorio = './Ajustes'
        
        try:
            os.stat(directorio)
        except:
            os.mkdir(directorio)
            
        os.chdir(directorio)
        plt.savefig("Gaussian "+hour[0][:9]+"_" +inp[13:-4])
        plt.show()

    elif model=='Poly' or model=='Polynomial' or model=='Pol' or model=='poly' or model=='pol' or model=='polynomial' or model=='poli':
        deg = int(input("Grado del polinomio: "))
        modelg = models.Polynomial1D(degree=deg)
        fitter = fitting.LevMarLSQFitter()
        ajusteg = fitter(modelg, totalsec, po)
        
        #modell = models.Lorentz1D(amplitude=0.5, x_0=300, fwhm=100)
        #fitter = fitting.LevMarLSQFitter()
        #ajustel = fitter(modell, totalsec, po)
        #if fitter.fit_info['message'] == 
        
        tope = 1.2 * max(po[150:-150])
        
        #vals.append((str(inp[6:-4]),ajusteg..value,ajusteg.mean.value, ajusteg.stddev.value))
    
        plt.figure(figsize=(13,10))
        plt.plot(totalsec.value, po, 'r.', label="Datos",linewidth=1,ms=4)
        plt.plot(totalsec.value, ajusteg(totalsec), 'b',label="Polynomial",linewidth=1,ms=4)
        #plt.plot(totalsec.value, ajustel(totalsec), 'g',label="Lorentziana",linewidth=1,ms=4)
        plt.ylim(0,tope)
        plt.xlim(0,600)
        plt.ylabel(r'Power (dBm)')
        plt.xlabel('Tiempo (s)')
        plt.title('Polynomial '+hour[0][:10]+"  " +inp[6:-4])
        
        chi = np.around(stats.chisquare(po,ajusteg(totalsec)).statistic,decimals=2)
            
        if chi =='nan' or chi>40000:
            chi = '-'
        
        plt.legend(title = "Ajuste:")
        texto = ("Chi² = "+str(chi))
        #pars.append((inp[6:-4],a,b,c,chi))
        medio = 6*tope/8
        plt.text(520, medio, texto, size=13, ha="center", va="center")
            
        directorio = './Ajustes'
        
        try:
            os.stat(directorio)
        except:
            os.mkdir(directorio)
            
        os.chdir(directorio)
        plt.savefig("Polynomial "+hour[0][:9]+"_" +inp[6:-4])
        plt.show()
    
    #ax.imsave("ajuste" +hour[0][:10]+"  " +inp[5:-4])
    #ax.show()
    return 
