#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import bokeh

import geopandas as gpd
import pandas as pd

from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, Slider, HoverTool
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, row, column


# In[2]:


stateshape = gpd.read_file('D:\Trimester 2 APU (2nd Year)\Intermediate_Microeconomics\States\Admin2.shp')
stateshape


# In[5]:


new_file = pd.read_csv('modified-HDI.csv')
new_file.head(55)


# In[6]:


#Define function that returns json_data for year selected by user.
    
def json_data(selectedYear):
    yr = selectedYear
    df_yr = new_file[new_file['Year'] == yr]
    merged = stateshape.merge(df_yr, on='ST_NM')
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return json_data
#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data(2018))
#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0.5, high = 1)
#Define custom tick labels for color bar.
tick_labels = {'0': '0', '0.4': '0.4', '0.5':'0.5', '0.6':'0.6', '0.7':'0.7', '0.8':'0.8', '0.9':'0.9','1':'1'}
#Add hover tool
hover = HoverTool(tooltips = [ ('State','@ST_NM'),('HDI', '@HDI')])
#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
#Create figure object.
p = figure(title = 'HDI of Indian States, 2018', plot_height = 600 , plot_width = 600, toolbar_location = None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'HDI', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p.add_layout(color_bar, 'below')
# Define the callback function: update_plot
def update_plot(attr, old, new):
    yr = slider.value
    new_data = json_data(yr)
    geosource.geojson = new_data
    p.title.text = 'HDI of Indian States, %d' %yr
    
# Make a slider object: slider 
slider = Slider(title = 'Year',start = 2000, end = 2018, step = 1, value = 2018)
slider.on_change('value', update_plot)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,bokeh.models.Column(slider))
curdoc().add_root(layout)
#Display plot inline in Jupyter notebook
output_notebook()
#Display plot
show(layout)

