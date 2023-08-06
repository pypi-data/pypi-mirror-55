#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:00:16 2019

@author: dmoral
"""

from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle, ITRS

hdulist = fits.open(input('Input FITS: '))

hp = HEALPix(nside=hdulist[0].header['NSIDE'],
             order=hdulist[0].header['ORDERING'],
             frame=AltAz())