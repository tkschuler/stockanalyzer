
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
import indicators
import argparse
import logging

__author__ = "Tristan Schuler"
__copyright__ = "The GNU General Public License v3.0"

# Terminal Arguments Parsing
parser = argparse.ArgumentParser(description='StockAnalyzer Plot Parameters')

parser.add_argument('--ticker', nargs='?', type=str, required = True,
                help='Choose a ticker to show a plot foor')

parser.add_argument('--days', nargs='?', type=int, default = 180,
                help='How many days to show historical stock data')

args = parser.parse_args()
if args.ticker is None :
    parser.error("--ticker required")

# Formatting:
pd.set_option("display.max_rows", None)
SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

ticker_df = pd.read_csv("Stocks/" + args.ticker + ".csv")
df = ticker_df
Company = args.ticker

# Determine indicators
rsi = indicators.RSI(ticker_df, 7)
d,k  = indicators.STOCH(ticker_df)
macd_df, signal_df = indicators.MACD(ticker_df)

ticker_df['RSI'] = rsi
ticker_df['D'] = d
ticker_df['K'] = k
ticker_df['MACD'] = macd_df
ticker_df['SIGNAL'] = signal_df
ticker_df = ticker_df.tail(args.days) # Reduce size of table to last n days,

fig = plt.figure(figsize = (17,10))
fig.suptitle(str(args.days) + " Day Indicators for " + Company, fontsize=14)

ax = plt.subplot(4, 1, 1)
ax2 = plt.subplot(4, 1, 2, sharex=ax)
ax4 = plt.subplot(4, 1, 4, sharex=ax)
ax3 = plt.subplot(4, 1, 3, sharex=ax)

plot1, = ax.plot(ticker_df['Date'], ticker_df['Close'])
plot2, = ax2.plot(ticker_df['Date'], ticker_df['RSI'])
plot4, =  ax4.plot(ticker_df['Date'][-len(ticker_df['MACD']):], ticker_df['MACD'], 'r')
plot4, =  ax4.plot(ticker_df['Date'][-len(ticker_df['SIGNAL']):], ticker_df['SIGNAL'], 'b')
plot3, = ax3.plot(ticker_df['Date'], ticker_df['D'])


ax2.axhspan(50, 100, alpha=0.2, color='green')
ax2.set_ylim(0,100)
ax3.axhspan(50, 100, alpha=0.2, color='green')


#ticker formatting
ax.set_xlim((date.today()-timedelta(days=args.days)).strftime("%Y-%m-%d"), (date.today()+timedelta(days=2)).strftime("%Y-%m-%d"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

# Cursor for looking at all subplots
multi = MultiCursor(fig.canvas, (ax, ax2, ax3, ax4), color='r', lw=1)

ax.title.set_text('Stock Price')
ax2.title.set_text('RSI (7)')
ax3.title.set_text('Stochastics (14, 3)')
ax4.title.set_text('MACD (12, 26)')

fig.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()
