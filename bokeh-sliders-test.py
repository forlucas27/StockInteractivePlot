from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, TextInput, Select
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import requests
import datetime
import json
from pandas import DataFrame
import pandas as pd
from time import strptime

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-histories"

# inputs
symbol = 'TSLA'

start_string = "01/01/2020"
start_date = datetime.datetime.strptime(start_string, "%m/%d/%Y")
start = datetime.datetime.timestamp(start_date)
# print(int(start))

end_string = "02/01/2020"
end_date = datetime.datetime.strptime(end_string, "%m/%d/%Y")
end = datetime.datetime.timestamp(end_date)


def get_history(symbol, start, end):
    # print(start)
    # print(end)
    querystring = {"symbol": symbol, "from": str(int(start)), "to": str(
        int(end)), "events": "div", "interval": "1d", "region": "US"}
    # "1546448400" "1562086800"

    headers = {
        'x-rapidapi-key': "47448f53d2msh984fd854b0e692ep1c0ee3jsn12cf61e73b75",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    data = response.text
    #data1 = data.decode("utf-8")
    data1 = json.loads(data)

    timestamp_df = DataFrame(data1['chart']['result'][0]['timestamp'])
    # print(timestamp_df)
    timestamps = pd.to_datetime(timestamp_df[0], unit='s')
    # print(timestamps)

    close = np.array(data1['chart']['result'][0]
                     ['indicators']['quote'][0]['close'])

    return timestamps, close


''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
#from os.path import dirname, join


# Set up data
N = 200
#x = np.linspace(0, 4*np.pi, N)
#y = np.sin(x)

start_string = "01/01/2020"
start_date = datetime.datetime.strptime(start_string, "%m/%d/%Y")
start = datetime.datetime.timestamp(start_date)
# print(int(start))

end_string = "02/01/2020"
end_date = datetime.datetime.strptime(end_string, "%m/%d/%Y")
end = datetime.datetime.timestamp(end_date)


x, y = get_history('TSLA', start, end)
# print(x)
# print(x,y)

#x = timestamps
#y =np.array(data1['chart']['result'][0]['indicators']['quote'][0]['close'])

source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="Closing Price Over One Month",
              tools="crosshair,pan,reset,save,wheel_zoom", x_axis_type='datetime')
# x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="Stock Symbol", value='TSLA')
#offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
#amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
#phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
#freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)
month = Select(title="Month", value="Jan",
               options=open('months.txt').read().split())
year = TextInput(title="Year", value='2020')


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

#text.on_change('value', update_title)
#text.on_change('value', update_title)


def update_data(attrname, old, new):

    # Get the current slider values
    #a = amplitude.value
    #b = offset.value
    #w = phase.value
    #k = freq.value

    # Generate the new curve
    #x = np.linspace(0, 4*np.pi, N)
    #y = a*np.sin(k*x + w) + b
    # print(text.value)
    m = month.value
    # print(m)
    m = strptime(m, '%b').tm_mon
    # print(m)

    y = year.value
    # print(y)

    start_string = str(m) + '/01/' + str(y)
    # print(start_string)
    end_string = str(m+1) + '/01/' + str(y)
    # print(end_string)

    start_date = datetime.datetime.strptime(start_string, "%m/%d/%Y")
    start = datetime.datetime.timestamp(start_date)

    end_date = datetime.datetime.strptime(end_string, "%m/%d/%Y")
    end = datetime.datetime.timestamp(end_date)

    x, y = get_history(text.value, start, end)
    #x, y = get_history('TSLA')

    #x = timestamps
    #y =np.array(data1['chart']['result'][0]['indicators']['quote'][0]['close'])

    source.data = dict(x=x, y=y)


text.on_change('value', update_data)
month.on_change('value', update_data)
year.on_change('value', update_data)

# for w in [offset, amplitude, phase, freq]:
#    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = column(text, month, year)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
