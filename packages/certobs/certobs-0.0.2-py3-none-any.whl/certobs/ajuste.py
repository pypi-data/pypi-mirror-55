#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:45:35 2019

@author: dmoral
"""
from astropy.modeling import models, fitting
from matplotlib import pyplot as plt
import numpy as np
import astropy.units as u
import os
from glob import glob
from scipy import stats

d = input("Directorio del archivo de potencias: ")
os.chdir(d)

pars = []



gl = glob('power*')

for i in gl:
    fit(i)
    
np.savetxt("pars.dat",pars,fmt='%5.6s',
           header=('SOURCE AMPLITUDE MEAN STDDEV CHI-SQUARE\n####################################' ))
#para que guarde esos datos hay que meterlo dentro de la función y correr la función como un bloque,
#aladiendole esto al principio: gl= glob('power*')  ; no llamándola como fit()
#yerr = 0.001
#N = len(totalsec)
#n_free = 4
#x = totalsec.value
#y = po
#fit = ajusteg
#
#def calc_reduced_chi_square(fit, x, y, yerr, N, n_free):
#    '''
#    fit (array) values for the fit
#    x,y,yerr (arrays) data
#    N total number of points
#    n_free number of parameters we are fitting
#    '''
#    return 1.0/(N-n_free)*sum(((fit - y)/yerr)**2)
