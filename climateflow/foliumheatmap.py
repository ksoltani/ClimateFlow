"""
Visualise some climate data with folium

@author: Nick Gibbons
"""


import folium
from folium import plugins
import numpy as np
from collateData import loadDicts, plotFormat, getChosenData


sDir, sYDir = loadDicts(2)
stationdata = getChosenData(8, 1992, sYDir, sDir)
lat, lon, temp = plotFormat(stationdata)

data = np.zeros((len(lat), 3))
data[:,0] = lat
data[:,1] = lon
data[:,2] = temp

#data = (np.random.normal(size=(100, 3)) *
#        np.array([[1, 1, 0.01]]) +
#        np.array([[-27.45, 153.02, 0.00]])).tolist()
#data[:50] += np.array([5.0, 10.0, 0.99])

osm_map = folium.Map(location=[-27.45, 153.02])
osm_map.add_child(plugins.HeatMap(data, max_val=25))
osm_map.save('./heatmap.html')
