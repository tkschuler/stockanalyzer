
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

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)



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
        if ticker_df.iloc[c,4] > float(2.00):  # Check that the closing price for this day is greater than $2.00
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

list_files = (glob.glob("Stocks/*.csv"))
for stock in list_files:

    ticker_df = pd.read_csv(stock)
    df = ticker_df
    Company = ((os.path.basename(stock)).split(".csv")[0])

    df['RSI'] = RSI(ticker_df, 7)
    df['D'],df['K']  = STOCH(ticker_df)
    macd_df, signal_df = MACD(ticker_df)


    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("6 Month Indicators for " + Company, fontsize=14)

    ax = plt.subplot(4, 1, 1)
    ax2 = plt.subplot(4, 1, 2, sharex=ax)
    ax4 = plt.subplot(4, 1, 4, sharex=ax)
    ax3 = plt.subplot(4, 1, 3, sharex=ax)

    plot1, = ax.plot(df['Date'][-180:], df['Close'][-180:])
    plot2, = ax2.plot(df['Date'][-180:], df['RSI'][-180:])
    plot4, =  ax4.plot(df['Date'][-180:], macd_df[-180:], 'r')
    plot4, =  ax4.plot(df['Date'][-180:], signal_df[-180:], 'b')
    plot3, = ax3.plot(ticker_df['Date'][-180:], df['D'][-180:])
    plot3, = ax3.plot(ticker_df['Date'][-180:], df['K'][-180:])

    ax.set_ylim(df['Close'].tail(180).min()-2 ,df['Close'].tail(180).max()+2)
    ax2.axhspan(50, 100, alpha=0.2, color='green')
    ax2.set_ylim(0,100)
    ax3.axhspan(50, 100, alpha=0.2, color='green')

    '''
    ax.set_xlim((date.today()-timedelta(days=150)).strftime("%Y-%m-%d"), (date.today()).strftime("%Y-%m-%d"))
    ax2.set_xlim((date.today()-timedelta(days=150)).strftime("%Y-%m-%d"), (date.today()).strftime("%Y-%m-%d"))
    ax3.set_xlim((date.today()-timedelta(days=150)).strftime("%Y-%m-%d"), (date.today()).strftime("%Y-%m-%d"))
    ax4.set_xlim((date.today()-timedelta(days=150)).strftime("%Y-%m-%d"), (date.today()).strftime("%Y-%m-%d"))
    '''

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    ax3.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    multi = MultiCursor(fig.canvas, (ax, ax2, ax3, ax4), color='r', lw=1)

    ax.title.set_text('Stock Price')
    ax2.title.set_text('RSI (7)')
    ax3.title.set_text('Stochastics (14, 3)')
    ax4.title.set_text('MACD (12, 26)')

    plt.show()
