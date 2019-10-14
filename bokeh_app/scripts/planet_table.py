# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
from bokeh.layouts import row, column, widgetbox, gridplot, layout

from bokeh.models import ColumnDataSource, Panel, CustomJS, LayoutDOM
from bokeh.models.widgets import TableColumn, DataTable, TextInput, Paragraph, Button
from bokeh.plotting import figure
from bokeh.palettes import Spectral3
from bokeh.models.widgets import Div
from bokeh.transform import factor_cmap


def table_planet(planets):
    # Calculate summary stats for table
    planet_stats = pd.crosstab(planets.Planet, planets.Males)
    planet_stats = planet_stats.reset_index().rename(
        columns={0: 'Females', 1: 'Males', 'Planet': 'Planets'})
    planet_stats['Total'] = planet_stats['Males'] + planet_stats['Females']

    # statistics for display

    planet_src = ColumnDataSource(planet_stats)

    # Columns of table
    table_columns = [TableColumn(field='Planets', title='Planets'),
                     TableColumn(field='Females', title='Females'),
                     TableColumn(field='Males', title='Males'),
                     TableColumn(field='Total', title='Total')]

    carrier_table = DataTable(source=planet_src,
                              columns=table_columns, width=1200, height=200)

    # from bokeh.io import show, output_notebook
    # from bokeh.plotting import figure
    #
    # Total_bar = ['Total Males', 'Total Females', 'Total people']
    # T_males = sum(planet_stats['Males'])
    # T_females = sum(planet_stats['Females'])
    # T_Total = T_males + T_females
    #
    # # Set the x_range to the list of categories above
    # p = figure(x_range=Total_bar, plot_height=250,toolbar_location=None, title="Total  Counts")
    #
    # # Categorical values can also be used as coordinates
    # p.vbar(x=Total_bar, top=[T_males, T_females, T_Total],legend='Total_bar', width=0.9)
    # p.legend.orientation = "horizontal"
    # p.legend.location = "top_center"
    #
    # # Set some properties to make the plot look better
    # p.xgrid.grid_line_color = None
    # p.y_range.start = 0
    # -------------------------------------------------------------
    # Interactive Bar Chart to display Totals

    # =============================================================

    Total_bar = ['Total Males', 'Total Females', 'Total people']

    T_males = sum(planet_stats['Males'])
    T_females = sum(planet_stats['Females'])
    T_Total = T_males + T_females
    val = [T_males, T_females, T_Total]

    source = ColumnDataSource(data=dict(Total_bar=Total_bar, val=val, color=Spectral3))

    barchart = figure(x_range=Total_bar, y_range=(0, 210), plot_height=400, plot_width=700,
                      title="Total Species Count",
                      toolbar_location=None, tools="")

    barchart.vbar(x='Total_bar', top='val', width=0.5, color='color', legend='Total_bar', source=source)

    barchart.min_border_top = 0
    barchart.min_border_bottom = 0
    barchart.min_border_right = 20
    barchart.margin = 10
    # Here we change the position of the legend in the graph
    # Normally it is displayed as a vertical list on the top
    # right. These settings change that to a horizontal list
    # instead, and display it at the top center of the graph
    barchart.legend.orientation = "horizontal"
    barchart.legend.location = "top_center"
    barchart.legend.click_policy = "hide"

    # -------------------------------------------------------------
    # widget for population scaling output

    # =============================================================
    a = 0
    b = a

    # PREP DATA
    welcome_message = 'You have entered: (none)'

    # TAKE ONLY OUTPUT
    text_banner = Paragraph(text=welcome_message, width=200, height=50)
    text_banner_bs = Paragraph(width=200, height=8)
    validation_flag = False

    # callbacks

    callback_a = CustomJS(code="""

            var f = cb_obj.value
            a=f

            source.change.emit();
        """)
    callback_b = CustomJS(code="""
            var f = cb_obj.value
            b=f

            source.change.emit();
            """)

    def callback_ans(text_banner=text_banner):

        v = ((float(a) * 200) / (float(b) * 200)) ** 2

        if (2 < float(a) < 10000) and (2 < float(b) < 10000):
            message = 'the population scaling value is: ' + str(v)

            print('from button', str(v))
        else:
            message = 'ERROR!!! please enter input range from 2 to 10000 '

        # welcome_message = 'You have selected: ' + user_input
        text_banner.text = message

    # USER INTERACTIONS
    text_input = TextInput(value="", title="Enter value of a :")
    text_input2 = TextInput(value="", title="Enter value of b:")
    text_input.js_on_change('value', callback_a)
    text_input2.js_on_change('value', callback_b)

    button = Button(label="Population Scaler", button_type="success", callback=CustomJS.from_py_func(callback_ans))

    # -------------------------------------------------------------------------------

    # widget LAYOUT
    widg = widgetbox(text_banner_bs,text_input, text_input2, text_banner, button)
    # -------------------------------------------------------------------------------
    # div for introductory text
    div = Div(text="""<h3>Hello..Thanks for stopping by the........? <span class="fr-emoticon fr-deletable fr-emoticon-img" style="background: url(https://cdnjs.cloudflare.com/ajax/libs/emojione/2.0.1/assets/svg/1f600.svg);">&nbsp;</span></h3>
<h2>Hitch Hikers Planetary species Data Set</h2>
<p><span style="font-family: Arial, Helvetica, sans-serif;">Fictitious data-set of male sample populations of a rare species of lifeform. It is assumed that there are only 2 sexes, male and female.The above table represents population of species across different planets. Click on any title to order data in ascending or descending order.The below bar chart is an interactive representation of total counts of species .</span></p>
<p><span style="font-family: Arial, Helvetica, sans-serif;">Using the widgetbox the user can perform an arbitrary calculation called &lsquo;Population Scaling&rsquo; which is (a * x)/(b-1)^2 , (where x is the result computed in ToltalPopulation), a and b are floating point numbers in the range [2,10000]. &nbsp;The user is expected &nbsp;to enter values for a and b in the interface and click a button to see the result.</span></p>""",
              width=1200, height=200)

    # -------------------------------------------------------------------------------

    # Create a row layout
    lay = column(carrier_table, column(div, row(barchart, widg)))
    # l = gridplot([
    #     [carrier_table],
    #     [barchart, widg],
    # ], sizing_mode='scale_both')

    # tab = Panel(child=carrier_table, title='Summary Table')
    tab = Panel(child=lay, title='Summary Table')

    return tab
