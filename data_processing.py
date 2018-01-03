# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 18:02:38 2017

@author: Connor
"""
import pdb
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

def processCensus(df1):
    counties = list(df1['county'].values)
    stName = list(df1['st'].values)
    stFIPS = list(df1['stfips'].values)
    
    newID = [st+'-'+str(stFIP)+'-'+str(county) for st, stFIP, county in zip(stName,
             stFIPS, counties)]
    df1['county_combo'] = newID
    newCounties = list(set(df1['county_combo'].values))
    
    resultsDict = {}
    
    for county in newCounties:
        dfCounty = df1[df1['county_combo'] == county]
        years = np.sort(list(set(dfCounty['year'].values)))
        countyYearDict = {}
        interimDict = {}
        print(county)
        
        for year in years:
            #print(year)
            dfYear = dfCounty[dfCounty['year'] == year]
            raceSum = dfYear.groupby('race').sum()
            
            raceSumStorage = []
            for idx in raceSum.index:
                raceValues = raceSum.loc[idx]
                               
                if year == np.min(years):
                    interimDict[idx] = [raceValues['pop'], 0]
                    
                else:
                    interimDict[idx] = [raceValues['pop'], raceValues['pop']-interimDict[idx][0]]
    
            for i in range(1,4):
                if i in raceSum.index:
                    pass        
                else:
                    interimDict[i] = [0,0]
                    
            for key in interimDict:
                raceSumStorage.extend(interimDict[key])
                
            countyYearDict[year] = raceSumStorage
            
        resultsDict[county] = countyYearDict
            
    results = []
    
    for county in resultsDict:
        countyDict = resultsDict[county]
        
        for year in countyDict:
            yearValues = countyDict[year]
            resultValues = [county, year]
            resultValues.extend(yearValues)
            results.append(resultValues)
            
    df3 = pd.DataFrame(results, columns = ['County', 'Year', 'wp', 'wc',
                                           'bp', 'bc', 'op', 'oc'])

    return(df3)

#df1 = pd.read_csv(r'D:\old desktop\Development\uswbo19agesadj.csv')  
#pdb.set_trace()


#dfResults = processCensus(df1)    
#dfResults.to_csv('resultsnewcensus.csv')


dfResults = pd.read_csv('resultsnewcensus.csv')

df3 = dfResults
df3['b_pct_c'] = (df3['bp']/(df3['bp']-df3['bc'])-1)
df3['w_pct_c'] = (df3['wp']/(df3['wp']-df3['wc'])-1)
df3 = df3.replace([np.inf, -np.inf], np.nan)
df3 = df3.dropna()

df3['sign_diff'] = np.sign(df3['b_pct_c']) + np.sign(df3['w_pct_c'])
df3['total_all'] = df3['wp']+df3['bp']+df3['op']

df3['bpt'] = df3['bp'] + (-1*df3['bc'])
df3.to_csv('modified_results.csv')

dfBC = df3[df3['total_all'] > 50000]
dfBC = dfBC[dfBC['bpt'] > 200]

dfBC = dfBC[dfBC['sign_diff'] != 2]
dfBC = dfBC[dfBC['sign_diff'] != -2]

dfLoss = dfBC[dfBC['b_pct_c'] < -0.1]
dfGain = dfBC[dfBC['b_pct_c'] > 0.5]



dfJeff = dfResults[dfResults['County'] == 'NY-36-36045']

plt.plot(dfJeff['Year'].values, dfJeff['wc'].values, label='White Pop Change', color='orange', linewidth=4)
plt.plot(dfJeff['Year'].values, dfJeff['bc'].values, label='Black Pop Change', color='brown', linewidth=4)
plt.legend()
plt.xlabel('Year')
plt.ylabel('Population Change from Previous Year')
plt.grid(True)
plt.savefig('jeff_all.png', dpi=300)

#plt.show()
#
#dfBC_loss = dfBC[dfBC['b_pct_c'] < -0.1]
#dfBC_gain = dfBC[dfBC['b_pct_c'] > 1]
















