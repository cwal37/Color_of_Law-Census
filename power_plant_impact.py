# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:40:53 2018

@author: Connor
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb, os, sys, time, random


powerData = pd.read_csv(r'powerPlants\plantRetirements.csv')
censusData = pd.read_csv(r'modified_results.csv')
countyMapping = pd.read_csv(r'county_mapping.csv', encoding = "ISO-8859-1")

stAbbvs = list(countyMapping['State Abbrev'].values)
stNs = list(countyMapping['State Code (FIPS)'].values)
countyNs = list(countyMapping['County Code (FIPS)'].values)

countyMapping['census_code'] = [state+'-'+str(stateN)+'-'+str(stateN)+str(countyN) for state, stateN, countyN in zip(stAbbvs, stNs, countyNs)]

dirtyFuels = ['DFO', 'SUB', 'JF', 'BIT', 'LIG', 'RFO', 'OBS', 'KER', 'BFG', 'BLQ']

dirtyGen = powerData[powerData['Energy Source 1'].isin(dirtyFuels)]
dirtyGen = dirtyGen[dirtyGen['Retirement Year'] >= 1970]
dirtyGen.sort_values('Operating Year', ascending=True)
