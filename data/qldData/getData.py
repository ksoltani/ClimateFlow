import urllib
import urllib2
from bs4 import BeautifulSoup
from time import sleep

#-----------------------------------------------------
# code to import station number and longitude/latitude
#-----------------------------------------------------
stationsFile = open('alphaQLD_36.txt','r')
lines = stationsFile.readlines()
stationCode = []
codeColStart = lines[2].find('Site')
nameColStart = lines[2].find('Name')
latColStart= lines[2].find('Lat')
lonColStart = lines[2].find('Lon')
startColStart = lines[2].find('Start')
endColStart = lines[2].find('End')
yearsColStart = lines[2].find('Years')
percentColStart = lines[2].find('%')
awsColStart = lines[2].find('AWS')
labelsList = ['Site', 'Name', 'Lat', 'Lon', 'Start', 'End', 'Years', '%', 'AWS']
index = {} # Use this dictionary along the above labels to read data from the list
c = 0
for i in labelsList:
    index[i] = c
    c = c + 1
dataLines = lines[4:]
stationsData = []
for l in dataLines:
    code = l[0:nameColStart].strip()
    if len(code) < 6:
        code = (6 - len(code)) * '0'+code
    name = l[nameColStart:latColStart].strip()
    lat = l[latColStart:lonColStart].strip()
    lon = l[lonColStart:startColStart].strip()
    start= l[startColStart:endColStart].strip()
    end = l[endColStart:yearsColStart].strip()
    years = l[yearsColStart:percentColStart].strip()
    percent = l[percentColStart:awsColStart].strip()
    aws = l[awsColStart:].strip()
    data = [code, name, lat, lon, start, end, years, percent, aws]
    stationsData.append(data)
 
#-----------------------------------------------
# code to scrape website 
#-----------------------------------------------
for i in range(0, len(stationsData), 1):
    sleep(3.0)
    print i
    temp = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=36&p_display_type=dataFile&p_startYear=&p_c=&p_stn_num='+stationsData[i][0]
    r = urllib.urlopen(temp).read()
    print temp
    soup = BeautifulSoup(r, 'html.parser')
    try:
        webpage = str((soup.find(text='Monthly mean maximum temperature').findNext('li').findNext('li').a.get("href")))
        webpage = "http://www.bom.gov.au" + webpage
        #-----------------------------------------------
        # code to download file from url
        #-----------------------------------------------
        urllib.urlretrieve (webpage, stationsData[i][0]+".zip")
    except Exception:
        continue
    
