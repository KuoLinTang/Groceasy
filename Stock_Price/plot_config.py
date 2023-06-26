import io
import base64
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from stockdata import StockData
# Avoid UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
matplotlib.use('agg')


def slice_data(stock_data: StockData, measure: str, period: str):
    today = datetime.now()

    if period == "1_year":
        start_date = today - pd.DateOffset(years=1)
    elif period == "2_years":
        start_date = today - pd.DateOffset(years=2)
    elif period == "6_months":
        start_date = today - pd.DateOffset(months=6)
    elif period == "1_month":
        start_date = today - pd.DateOffset(months=1)
    elif period == "1_day":
        current_stock = stock_data.stock_code
        hourly_data = StockData(current_stock, period='1d', interval='1m')
        if measure == 'Volume':
            dataframe_for_plot = hourly_data.get_volume()
        else:
            dataframe_for_plot = hourly_data.get_close_price()
        return dataframe_for_plot
    else:
        # period is MAX
        if measure == 'Volume':
            dataframe_for_plot = stock_data.get_volume()
        else:
            dataframe_for_plot = stock_data.get_close_price()
        return dataframe_for_plot

    if measure == 'Volume':
        dataframe_for_plot = stock_data.get_volume()
    else:
        dataframe_for_plot = stock_data.get_close_price()

    start_date = start_date.strftime('%Y-%m-%d')
    dataframe_for_plot = dataframe_for_plot[start_date:]
    return dataframe_for_plot


def plot_stock_data(stock_data, measure, period):

    dataframe_for_plot = slice_data(stock_data, measure, period)

    plt.figure(figsize=(14, 4))
    plt.plot(dataframe_for_plot, linewidth=1)

    if measure == "Price":
        plt.ylabel('Close Price (USD)')
    else:
        plt.ylabel('Volume')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return plot_data
