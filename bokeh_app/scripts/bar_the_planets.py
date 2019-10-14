from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import ColumnDataSource, Panel
import pandas as pd
from bokeh.models.widgets import Div
import numpy as np
from bokeh.models.widgets import TableColumn, DataTable


def bar_tab(planets):
    # Calculate summary stats for table
    planet_stats = pd.crosstab(planets.Planet, planets.Males)
    planet_stats = planet_stats.reset_index().rename(
        columns={0: 'Females', 1: 'Males', 'Planet': 'Planets'})
    planet_stats['Total'] = planet_stats['Males'] + planet_stats['Females']
    planets = planet_stats['Planets']
    data = {'planets': planets,
            'males': planet_stats['Males'],
            'females': planet_stats['Females'],
            'total': planet_stats['Total']}
    print(data)

    source = ColumnDataSource(data=data)

    p = figure(x_range=planets, y_range=(0, 50), plot_height=600, plot_width=1200, title="Total Species composition",
               toolbar_location=None, tools="")

    p.vbar(x=dodge('planets', -0.25, range=p.x_range), top='males', width=0.2, source=source,
           color="#c9d9d3", legend=value("males"))

    p.vbar(x=dodge('planets', 0.0, range=p.x_range), top='females', width=0.2, source=source,
           color="#718dbf", legend=value("females"))

    p.vbar(x=dodge('planets', 0.25, range=p.x_range), top='total', width=0.2, source=source,
           color="#e84d60", legend=value("total"))

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.legend.click_policy = "hide"
    # -------------------------------------------------------------------------------
    # div for introductory text
    div = Div(text="""<h2>Dodged Bar chart with interactive legend</h2> <p>The below bar chart displays the species data 
    across individual planets at the same time.</p> <p>Also this has an interactive legend, i.e ,clicking or tapping 
    on the legend entries will hide or mute the corresponding glyph in a plot. &nbsp;</p>""",
              width=1200, height=110)

    # -------------------------------------------------------------------------------

    # Create a row layout
    lay = column(div, p)

    tab = Panel(child=lay, title='Bar Chart')

    return tab
