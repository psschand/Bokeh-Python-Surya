# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
from bokeh.layouts import row, column, widgetbox
from bokeh.layouts import widgetbox
from bokeh.models import CustomJS, TextInput, Paragraph, DataSource, ServerSentDataSource
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable, TextInput
from bokeh.plotting import figure, Figure
from bokeh.models.widgets import Button


def statistics_tab(planets):
    a = 0
    b = a


    # PREP DATA
    welcome_message = 'You have selected: (none)'

    # TAKE ONLY OUTPUT
    text_banner = Paragraph(text=welcome_message, width=200, height=100)
    validation_flag = False

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

        v = ((int(a) * 200) / (int(b) * 200)) ** 2

        if (2 < int(a) < 10000) and (2 < int(b) < 10000):
            message = 'the population scaling value is: ' + str(v)

            print('from button', str(v))
        else:
            message = 'ERROR!!! please enter input range from 2 to 1000 '

        # welcome_message = 'You have selected: ' + user_input
        text_banner.text = message

    # USER INTERACTIONS
    text_input = TextInput(value="", title="Enter value of a :")
    text_input2 = TextInput(value="", title="Enter value of b:")
    text_input.js_on_change('value', callback_a)
    text_input2.js_on_change('value', callback_b)

    button = Button(label="Foo", button_type="success", callback=CustomJS.from_py_func(callback_ans))

    # -------------------------------------------------------------------------------------

    # LAYOUT
    widg = widgetbox(text_input, text_input2, text_banner, button)

    # --------------------------------------------------------------------------------

    # Create a row layout
    layout = column(widg, widg)

    # tab = Panel(child=carrier_table, title='Summary Table')
    tab = Panel(child=layout, title='Summary Table')

    return tab
