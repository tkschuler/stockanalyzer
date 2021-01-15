import pandas as pd
pd.set_option('expand_frame_repr', False)
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
import time
import matplotlib.dates as mdates
import mplcursors
from matplotlib.widgets import MultiCursor
import os, glob
import yfinance as yahoo_finance

def RSI (ticker_df, time_window):
    diff = ticker_df['Close'].diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]

    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()

    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

def STOCH(ticker_df):
 STOK = ((ticker_df['Close'] - ticker_df['Low'].rolling(window=14).min()) / (ticker_df['High'].rolling(window=14).max()  - ticker_df['Low'].rolling(window=14).min())) * 100
 STOD = STOK.rolling(window=3).mean()
 return STOD, STOK


def MACD(ticker_df):

    prices = []
    c = 0
    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    while c < len(ticker_df):
        prices.append(ticker_df.iloc[c,4])
        c += 1
    prices_df = pd.DataFrame(prices)  # Make a dataframe from the prices list

    # Calculate exponentiall weighted moving averages:
    day12 = prices_df.ewm(span=12).mean()  #
    day26 = prices_df.ewm(span=26).mean()

    macd = []  # List to hold the MACD line values
    counter=0  # Loop to substantiate the MACD line
    while counter < (len(day12)):
        macd.append(day12.iloc[counter,0] - day26.iloc[counter,0])  # Subtract the 26 day EW moving average from the 12 day.
        counter += 1
    macd_df = pd.DataFrame(macd)


    signal_df = macd_df.ewm(span=9).mean() # Create the signal line, which is a 9 day EW moving average
    signal = signal_df.values.tolist()  # Add the signal line values to a list.\

    return macd_df, signal_df
