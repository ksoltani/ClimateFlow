from bokeh.charts import HeatMap, output_file, show
    
# (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
data = {'food': ['pizza']*3 + ['nachos']*3 + ['whiskey']*3,
        'food_count': [4, 5, 8, 1, 2, 4, 6, 5, 4],
        'sample': [1, 2, 3]*3}

hm = HeatMap(data, x='food', y='sample', values='food_count',
             title='food', stat=None)

output_file('heatmap.html')
show(hm)
