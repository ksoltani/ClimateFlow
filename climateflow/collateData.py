""" 
Collate a stack of .zip files into python

@author: Kyle Damm and Kianoosh Soltani
"""

import os
import shutil
from math import log
import zipfile
import os.path
import pickle

def makeDirectories(stationFilename):
    """ Return stationsDirectory and stationYearDirectory """
    with open(stationFilename, 'r') as stationsFile:
        lines = stationsFile.readlines()
    stationCode = []
    print(lines[2])
    codeColStart = lines[2].find('Site')
    nameColStart = lines[2].find('Name')
    latColStart= lines[2].find('Lat')
    lonColStart = lines[2].find('Lon')
    startColStart = lines[2].find('Start')
    endColStart = lines[2].find('End')
    yearsColStart = lines[2].find('Years')
    percentColStart = lines[2].find('%')
    awsColStart = lines[2].find('AWS')
    
    dataLines = lines[4:]
    stationsDirectory = {}
    # Go through the file and produce a list of all stations
    for l in dataLines:
        code = l[0:nameColStart].strip()
        if len(code) < 6:
            code = (6 - len(code)) * '0'+ code
        name = l[nameColStart:latColStart].strip()
        lat = l[latColStart:lonColStart].strip()
        lon = l[lonColStart:startColStart].strip()
        start= l[startColStart:endColStart].strip()
        end = l[endColStart:yearsColStart].strip()
        years = l[yearsColStart:percentColStart].strip()
        percent = l[percentColStart:awsColStart].strip()
        aws = l[awsColStart:].strip()
        #data = [code, name, lat, lon, start, end, years, percent, aws]
        stationsDirectory[code] = [name, lat, lon]
    stationYearDirectory = {}
    noDataStations = []
    # Find the stations that don't have data
    for s in stationsDirectory.keys():
        if not os.path.isfile(s+str('.zip')):
            noDataStations.append(s)
    
    # remove directories that don't have any data
    for c in noDataStations:
        stationsDirectory.pop(c)
    # Look through the directories
    for s in stationsDirectory.keys():
    
        monthArray = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        zip = zipfile.ZipFile(s+str('.zip'))
        zip.extractall()
        os.remove('IDCJAC0002_'+s+'_Note.txt')
        os.remove('IDCJAC0002_'+s+'_Data1.csv')
        filename = 'IDCJAC0002_'+s+'_Data12.csv'
        with open(filename, 'r') as f:
            lines = f.readlines()
            lines = lines[1:]
            count = 0
            for l in lines:
                cleanLine = l.strip().split(',') 
                data = cleanLine[3 : 15] # monthly data
                #data = list(map(makefloat(data)))
                year = cleanLine[2]
                # record the start year
                if count == 0:
                    startYear = year    
                #print(s)
                stationYearDirectory[(s, year)] = data # Year is the second index
                count = count + 1
            endYear = year # record the last year for station s
            # add startYear and endYear data to the station directory info
            stationsDirectory[s].append(startYear)
            stationsDirectory[s].append(endYear)

    return stationsDirectory, stationYearDirectory

def makefloat(string):
    """ Tolerant float conversion """
    try:
        num = float(string)
    except(ValueError):
        num = -322.0
    return num

def getChosenData(month, year ,stationYearDirectory, stationsDirectory):
    """ month : int
        year : int
        stationYearDirectory: dict generated from data files
        stationsDirectory: dict generated from data files
        returns -> list of lists [['lat', 'lon', 'temp']]
    """    
    result = []
    for s in stationsDirectory.keys():
        #print(stationsDirectory[s])
        stationStartYear = stationsDirectory[s][3]
        stationEndYear = stationsDirectory[s][4]
        stationIncluded = False
        # check if the file exists if not do not inlcude the station
        #if not os.path.isfile('IDCJAC0002_'+s+'_Data12.csv'):
        #    stationIncluded = False
        # check if the requested year is in the recorded period for the station
        # if yes include the station else do not include it    
        if year >= int(stationStartYear) and year <= int(stationEndYear):
                stationIncluded = True
        else:
            stationIncluded = False
        # if the station has been there for the year check if it has data for
        # that specific year. If yes take that and add it to the result.    
        if stationIncluded and (s, str(year)) in stationYearDirectory:
            # we need to check if the file for this exists
            lat = stationsDirectory[s][1]
            lon = stationsDirectory[s][2]
            temp = stationYearDirectory[(s, str(year))][month - 1]
            result.append([lat, lon, temp])
        
    return result

def plotFormat(data):
    """ Take the output of getChosenData and return 
    three arrays corresponding to plottable lat, long, maxtemp
    """
    lat, lon, temp = list(zip(*data))
    lat = list(map(makefloat, lat))
    lon = list(map(makefloat, lon))
    temp = list(map(makefloat, temp))
    return lat, lon, temp

def loadDicts(version=3):
   if version==3:
       ext = '.pickle'
   else:
       ext = '.pickle2'
   with open('sDir'+ext, 'rb') as handle:
       sDir = pickle.load(handle) 
   with open('sYDir'+ext, 'rb') as handle:
       sYDir = pickle.load(handle) 
   return sDir, sYDir


if __name__ == '__main__':
    sDir, sYDir = makeDirectories('alphaQLD_36.txt')
    with open('sDir.pickle', 'wb') as handle:
        pickle.dump(sDir, handle) 
    with open('sYDir.pickle', 'wb') as handle:
       pickle.dump(sYDir, handle) 
    for i in range(1900, 1920, 1):        
        data= getChosenData(1, i, sYDir, sDir)
        print(data[0])

    data = getChosenData(8, 1992, sYDir, sDir)
    lat, lon, temp = plotFormat(data)
    print(lat[0:5], lon[0:5], temp[0:5])
