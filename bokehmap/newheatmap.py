from bokeh.charts import HeatMap, output_file, show
from numpy import linspace, random
    
# (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
data = {'x': linspace(1,4.0,50),
        'y': linspace(2,3,50),
        'temp': random.random(50)}

hm = HeatMap(data, x='x', y='y', values='temp',
             title='No longer food', stat=None)

output_file('heatmap.html')
show(hm)
