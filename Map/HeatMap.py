

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool, CustomJS
import pandas as pd
from bokeh.io import output_notebook
import numpy as np
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, ResetTool, RedoTool, UndoTool
)
from bokeh.models import GeoJSONDataSource
output_notebook()


#Get Data
df = pd.read_csv("final_no_outlier")

latitude = df['latitude'].tolist()
longitude = df['longitude'].tolist()
price = df['price per room'].tolist()
r = [0.0003] * len(price)
address = df['address'].tolist()
distance = df['edge_distance'].tolist()
sqft = df['sqft per room'].tolist()
food = df['avg_rating'].tolist()
cafes = df['#cafes'].tolist()
pubs = df['#pubs'].tolist()


# Create color span based on price
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
num_color = len(colors)
# create a price range list correspond to the color range list
max_price = max(price)
min_price = min(price)
interval = (max_price - min_price) / num_color
price_range = []
for i in range(num_color + 1):
    price_range.append(min_price + i * interval)
# give color to each location
loc_color = []
for p in price:
    for i in range(num_color):
        if p >= price_range[i] and p <= price_range[i + 1]:
            loc_color.append(colors[i])
            break


# Plot and google map 
map_options = GMapOptions(lat=37.87, lng=-122.27, map_type="roadmap", zoom=14)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Austin", plot_width=1200, plot_height=600,
    webgl=True
)

source = ColumnDataSource(
    data=dict(
        lat = latitude,
        lon = longitude,
        color = loc_color,
        rprice = price,
        dis = distance,
        addr = address,
        restaurant = food,
        cafe = cafes,
        pub = pubs,
        size = sqft,
    )
)
circle = Circle(x = 'lon', y = 'lat', fill_color = 'color', size = 10, fill_alpha=0.6, line_color=None)
plot.add_glyph(source, circle)

# Hover
hover = HoverTool()
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Address", "@addr"),
    ("Price per Room", "@rprice"),
    ("Distance to Campus", "@dis"),
    ("Food Quality", "@restaurant"),
    ("Number of cafes", "@cafe"),
    ("Number of pubs", "@pub"),
    ("Room size", "@size"),
]

tools = [PanTool(), WheelZoomTool(), hover]
plot.add_tools(*tools)

output_file("gmap_plot.html")
show(plot)