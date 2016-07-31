"""
Census example from datashader docs

@author: Nick Gibbons
"""
import datashader as ds
import datashader.transfer_functions as tf
import numpy as np
import pandas as pd
from datashader.utils import export_image
from datashader.colors import colormap_select, Greys9, Hot, viridis, inferno
from IPython.core.display import HTML, display

print("Begin...")
#df = pd.read_hdf('census.h5', 'census')

USA =          ((-13884029,  -7453304), (2698291, 6455972))
plot_width  = int(1000)
plot_height = int(plot_width*7.0/12)

df = pd.DataFrame(
      {'meterswest': np.random.random(10000)*1000e3 + -10668666.5,
      'metersnorth': np.random.random(10000)*1000e3 + 4577131.5}
      )
print(df.tail())


background = "black"
display(HTML("<style>.container { width:100% !important; }</style>"))

print("Computing aggregate...")
cvs = ds.Canvas(plot_width, plot_height, *USA)
agg = cvs.points(df, 'meterswest', 'metersnorth')

print("Making Image ...")
cmap = colormap_select(Hot,0.2, reverse=(background!="black"))
interp = tf.interpolate(agg, cmap = cmap, how='eq_hist')
export_image(interp, "census_ds_hot_eq_hist", background=background)


