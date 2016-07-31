# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 20:50:19 2016

@author: kianoosh
"""
from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)
from os.path import dirname, join
from bokeh.client import push_session
from bokeh.io import curdoc, vform, output_file
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox, row
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.models import Div
import sys
sys.path.insert(0, '../data/qldData')
from collateData import *

val = 2016
sDir, sYDir = loadDicts()
data = getChosenData(1, val, sYDir, sDir)
sLat, sLon, sTemp = plotFormat(data)

#output_file("gmap_plot.html")
map_options = GMapOptions(lat=-23, lng=144, map_type="roadmap", zoom=5)

plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, api_key = "AIzaSyATf-qiN-NRPnEUchZqGHEjPUYESAdjavY")
plot.title.text = "Queensland"
source = ColumnDataSource(
    data=dict(
        lat=sLat,
        lon=sLon,
    )
)

circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
slider = Slider(title="Time", value=2016, start=1900, end=2016, step=1)

controls = [slider]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = widgetbox(controls)
#p = figure(x_range=(-11, 11), y_range=(-11, 11))
curdoc().add_root(row(inputs, plot, width=1000))

#curdoc().add_root(plot)
#curdoc().title = "Sliders"


#show(plot)


## add slider ###
def time_select():
    val = slider.value
    print(val)
    data = getChosenData(1, val, sYDir, sDir)
    sLat, sLon, sTemp = plotFormat(data)
    print(len(data))
    #plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, api_key = "AIzaSyATf-qiN-NRPnEUchZqGHEjPUYESAdjavY")
    #plot.title.text = "Queensland"
    source.data = dict(
        lat=sLat,
        lon=sLon,
     )
    #circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)   
    #plot.add_glyph(source, circle)
    #source.trigger('data', source.data, source.data)
    return 


def update():
    time_select()
    return
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