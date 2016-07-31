"""
Census example from datashader docs

 -- Combined with mapping thing from example

@author: Nick Gibbons
"""
import datashader as ds
import datashader.transfer_functions as tf
import numpy as np
import pandas as pd
from datashader.utils import export_image
from datashader.colors import colormap_select, Greys9, Hot, viridis, inferno
from IPython.core.display import HTML, display
import bokeh.plotting as bp
from bokeh.models.tiles import WMTSTileSource
from datashader.bokeh_ext import InteractiveImage

def base_plot(prange, tools='pan,wheel_zoom,reset', webgl=False):
    p = bp.figure(tools=tools,
            plot_width=int(900*1.5), plot_height=int(500*1.5),
            x_range= prange[0],y_range=prange[1],
            outline_line_color=None,
            min_border=0, min_border_left=0, min_border_right=0,
            min_border_top=0, min_border_bottom=0, webgl=webgl)
    
    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    return p

def image_callback(x_range, y_range, w, h):
    cvs = ds.Canvas(
          plot_width=w,plot_height=h,x_range=x_range,y_range=y_range)
    agg = cvs.points(df,'meterswest','metersnorth')
    img = tf.interpolate(agg, cmap = cmap, how='eq_hist')
    return tf.dynspread(img,threshold=0.75, max_px=8)


print("Begin...")
#df = pd.read_hdf('census.h5', 'census') # Too big

background = "black"
USA =          ((-13884029,  -7453304), (2698291, 6455972))
plot_width  = int(1000)
plot_height = int(plot_width*7.0/12)

df = pd.DataFrame(
      {'meterswest': np.random.random(10000)*1000e3 + -10668666.5,
      'metersnorth': np.random.random(10000)*1000e3 + 4577131.5}
      )
print(df.tail())

display(HTML("<style>.container { width:100% !important; }</style>"))

bp.output_file('overlay.html',autosave=True)
p = base_plot(USA)

cmap = colormap_select(Hot,0.2, reverse=(background!="black"))
url="http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.png"
#url="http://tile.stamen.com/toner-background/{Z}/{X}/{Y}.png"
tile_renderer = p.add_tile(WMTSTileSource(url=url))
tile_renderer.alpha=1.0 if background == "black" else 0.15


InteractiveImage(p, image_callback, throttle=2000)
bp.save(p)

#
#print("Computing aggregate...")
#cvs = ds.Canvas(plot_width, plot_height, *USA)
#agg = cvs.points(df, 'meterswest', 'metersnorth')
#
#print("Making Image ...")
#interp = tf.interpolate(agg, cmap = cmap, how='eq_hist')
#export_image(interp, "census_ds_hot_eq_hist", background=background)


