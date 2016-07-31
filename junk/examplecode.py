from os.path import dirname, join import pandas as pd import numpy as np import pandas.io.sql as psql import sqlite3 as sql from bokeh.plotting import figure from bokeh.charts import HeatMap from bokeh.layouts import layout, widgetbox from bokeh.models import ColumnDataSource, HoverTool, Div from bokeh.models.widgets import Slider, Select, TextInput from bokeh.io import curdoc from IPython import embed from bokeh.palettes import Viridis256 data = pd.read_csv("ryt.csv") data['count'] = data['count'].astype(np.int64) desc = Div( text=open(join(dirname(__file__), "description.html")).read(), width=800) colors = Viridis256 def getcolor(g): try: maxc = rcount[g['Region']].values[0] # embed() if maxc != 0: idx=255 * (g['count'] / maxc) idx=idx.astype(np.int64) return pd.Series(np.array(colors)[idx]) else: return pd.Series(np.array(colors)[0 * g['count']]) except: pass # embed() rcount = data.groupby("Region")['count'].max() tmp = data.groupby(["Region","year"]).apply(getcolor) embed() data['color']= tmp.values years = sorted(data['year'].unique()) years = [str(year) for year in years] cat = sorted(data['Category'].unique()) # Create Input controls region = Select(title="region", options=sorted( data['Region'].unique()), value="Brisbane") # tmp=data[data['Region'] == region.value] # Create Column Data Source that will be used by the plot hover = HoverTool(tooltips=[ ("Region", "@Region"), ("Category", "@Category"), ("year", "@year"), ("count", "@count") ]) source = ColumnDataSource( data=dict(Region=[], Category=[], year=[], count=[], color=[])) # source = ColumnDataSource(data=dict(Region=tmp["Region"], Category=tmp["Category"], year=tmp["year"], count=tmp["count"])) TOOLS = "save,pan,resize" p = figure(x_range=years, y_range=cat, plot_height=800, plot_width=1200, title="Job Trend", tools=[hover,TOOLS]) p.rect('year', 'Category', 0.9, 0.9, color="color", source=source) # hm = HeatMap(source.data, x='year', y='Category', values='count', title='Job Trend', stat=None) def select_movies(): selected = data[data['Region'] == region.value] return selected def update(): df = select_movies() # p.xaxis.axis_label = sorted(df['year'].unique()) # p.yaxis.axis_label = sorted(df['Category'].unique()) source.data = dict( Region=df["Region"], Category=df["Category"], year=df["year"].astype(str), count=df["count"], color=df["color"] ) print source.data['color'] controls = [region] for control in controls: control.on_change('value', lambda attr, old, new: update()) sizing_mode = 'fixed' # 'scale_width' also looks nice with this example inputs = widgetbox(*controls, sizing_mode=sizing_mode) l = layout([ [desc], [inputs, p], ], sizing_mode=sizing_mode) update() # initial load of the data curdoc().add_root(l) curdoc().title = "Job Chart"