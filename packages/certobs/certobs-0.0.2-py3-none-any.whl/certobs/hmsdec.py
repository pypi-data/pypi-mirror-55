#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:57:39 2019

@author: dmoral
"""

# Write your hms2dec and dms2dec functions here
import numpy as np
from numpy import sign

def hms2dec(h,m,s):
  ra = (h + (m/60) + (s/3600))*15
  return ra

def dms2dec(d,m,s):
  dec = d + sign(d)*(m/60) + sign(d)*(s/3600)
  return dec
# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # The first example from the question
  print(hms2dec(23, 12, 6))

  # The second example from the question
  print(dms2dec(22, 57, 18))

  # The third example from the question
  print(dms2dec(-66, 5, 5.1))
  

def angular_dist(r1,d1,r2,d2):
  r1 = np.radians(r1)
  r2 = np.radians(r2)
  d1 = np.radians(d1)
  d2 = np.radians(d2)
  b = np.cos(d1)*np.cos(d2)*np.sin(np.abs(r1 - r2)/2)**2
  a = (np.sin(np.abs(d1-d2)/2))**2
  d = 2*np.arcsin(np.sqrt(a+b))
  d = np.degrees(d)
  return d


def import_bss():
  res = []
  bss = np.loadtxt('bss.dat', usecols=range(1, 7))
  for i, row in enumerate(bss, 1):
    res.append((i, hms2dec(row[0], row[1], row[2]), dms2dec(row[3], row[4], row[5])))
  return res

def import_super():
  data = np.loadtxt('super.csv', delimiter=',', skiprows=1, usecols=(0, 1))
  res = []
  for i, row in enumerate(data, 1):
    res.append((i, row[0], row[1]))
  return res