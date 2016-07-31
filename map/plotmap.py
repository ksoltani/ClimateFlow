"""
Checking the capabilities of folium

@author: Nick Gibbons
"""

import folium
from folium import plugins
import numpy as np

data = (np.random.normal(size=(100, 3)) *
        np.array([[1, 1, 1]]) +
        np.array([[-27.45, 153.02, 1]])).tolist()

osm_map = folium.Map(location=[-27.45, 153.02])
osm_map.add_child(plugins.HeatMap(data))
osm_map.save('./heatmap.html')


