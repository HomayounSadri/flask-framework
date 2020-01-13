from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.embed import components

def getData(ticker):
    # requesting data from Quandl
    start = "2018-01-01"
    end = "2018-01-31"
    reqUrl = 'https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '.json?start_date=' + start \
              + '&end_date=' + end + '&api_key=zYQbJBM9FNT9f71ngkz1'
    r = requests.get(reqUrl)

    # fetch data
    return_data = r.json()['dataset']
    df = pd.DataFrame(return_data['data'], columns=return_data['column_names'])
    df = df.set_index(pd.DatetimeIndex(df['Date']))
    return df


def getPlot(df, ticker):
    p = figure(title="Quandl WIKI EOD Stock Prices - January 2018", x_axis_type="datetime", x_axis_label="Date",
               y_axis_label="Stock price", plot_width=1000)

    p.line(df.index, df['Close'],legend_label=ticker)
    # show(p)
    return p


app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    # User inputs from the index.html
    ticker = request.form['ticker']
    ticker = ticker.upper()

    data = getData(ticker)
    plot = getPlot(data, ticker)

    script, div = components(plot)
    return render_template('graph.html', script=script, div=div)


if __name__ == '__main__':
    #  app.run(host='0.0.0.0', port=33507)
    app.run(port=33507)
