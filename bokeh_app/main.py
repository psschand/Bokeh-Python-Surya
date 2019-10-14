# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script


from scripts.planet_table import table_planet
from scripts.bar_the_planets import bar_tab
#from scripts.statistics import statistics_tab

# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
planets = pd.read_csv(join(dirname(__file__), 'data', 'planets_data.csv'), index_col=0).dropna()

# Create each of the tabs

tab1 = table_planet(planets)
tab2 = bar_tab(planets)
#tab3 = statistics_tab(planets)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
