import pandas as pd
import indicators
import glob, os
from datetime import date
from termcolor import colored

# Command line formatting for pandas dataframes:
pd.set_option("display.max_rows", None)
pd.options.mode.chained_assignment = None

today = date.today()
filename = today.strftime("redditscreens/%m-%d-%Y_redditscreen")

df = pd.read_csv(filename + '.csv', index_col = 'Code')

total = len(df) # keep track of how many stocks were included in the daily reddit screen for final stats

# Intially filter out penny stocks and stocks over $100.  (I don't have that kind of money for buying options... YET)
df = df[df.Price > 5]
df = df[df.Price < 100]
df = df[df.Volume > 500000]

df['Recommend'] = pd.Categorical(df['Recommend'], ["strong_buy", "buy", "hold", "0", "none", "sell", "strong_sell"])
filter = df[['Price','Total', '%Change','Rockets','Recommend']]
tickers = filter.index.tolist()
list_files = (glob.glob("Stocks/*.csv"))

for stock in list_files:
    try:

        ticker_df = pd.read_csv(stock)
        df = ticker_df
        Company = ((os.path.basename(stock)).split(".csv")[0])

        print(Company)

        # Solve for indicators for the lifespan of each ticker
        df['RSI'] = indicators.RSI(ticker_df, 7)
        df['D'],df['K']  = indicators.STOCH(ticker_df)
        df['MACD'], df['SIGNAL'] = indicators.MACD(ticker_df)

        allindicators = False
        i = 0

        # Check if all 3 indicators have been met (RSI > 50, Stochastics over 50, MACD Golden Cross passed)
        while not allindicators:
            rsi = df['RSI'].iloc[-i]
            d = df['D'].iloc[-i]
            macd = df['MACD'].iloc[-i] - df['SIGNAL'].iloc[-i]

            if macd < 0 or rsi < 0 or d < 0:
                filter.loc[Company, 'allindicators'] = i - 1
                allindicators = True
            else:
                i += 1


        rsi = None
        d = None

        # Check if RSI is above 50 for the latest closing price
        if df['RSI'].iloc[-1] > 50:
            rsi = True
        else:
            rsi = False

        # Check if Stochastics (only care about D) is above 50 for the latest closing price
        if df['D'].iloc[-1] > 50:
            d = True
        else:
            d = False

        # Detmine if MACD signal lines has been crossed, as well as the slope of the faster moving average
        macd = df['MACD'].iloc[-1] - df['SIGNAL'].iloc[-1]
        macd_slope = df['MACD'].iloc[-1] - df['MACD'].iloc[-2]
        macd_gc = macd_slope - macd

        GC = False # Golden Cross default
        if macd_slope > 0 and macd < 0:
            GC = True

        DC = False #Death Cross default
        if macd_slope < 0 and macd > 0:
            DC = True

        #Check if there was a Golden potential the past 2 days
        '''
        if (df['MACD'].iloc[-2] - df['MACD'].iloc[-3]) > 0 and df['MACD'].iloc[-2] - df['SIGNAL'].iloc[-2] < 0:
            GC = True
            '''

        #Add indicators to the full filtered table
        filter.loc[Company, 'RSI'] = rsi
        filter.loc[Company, 'D'] = d
        filter.loc[Company, 'MACD'] = macd
        filter.loc[Company, 'MACD_slope'] = macd_slope
        filter.loc[Company, 'MACD_gc'] = macd_gc
        filter.loc[Company, 'Gold+'] = GC
        filter.loc[Company, 'Death+'] = DC


    except:
        print(colored((Company + ' not imported'), 'red'))
        pass


#Remove Stocks that don't currently pass all 3 indicators, unless a possible Golden Cross is Present.
filter.drop(filter[(filter['allindicators'] <= 1) & (filter['Gold+'] == False)].index, inplace=True)
#Remove Death Crosses, We are looking for buying opportunities
filter.drop(filter[filter['Death+'] == True].index, inplace=True)
#Remove Stocks that do not satisfy all indicators and don't show a potential upcoming golden cross
filter.drop(filter[(filter['RSI'] == False) & (filter['Gold+'] == False)].index, inplace=True)
filter.drop(filter[(filter['D']   == False) & (filter['Gold+'] == False)].index, inplace=True)
#Drop stocks that the indicators couldn't be solved for (this is usually stocks that recently had an IPO)
filter = filter[filter['RSI'].notnull()]

# Sort by:  Golden Cross potential
#           How long all indicators have been met
#           Slope of the 12 Day avg  MACD slope
#           if RSI is above 50 (For sorting Golden Cross Potential)
#           if Stochastics are above 50 (For sorting Golden Cross Potential)

filter = filter.sort_values(['Gold+', 'allindicators', 'MACD_slope', 'RSI', 'D'] , ascending=[False,False, False, True, True])

filter.loc[filter['allindicators'] == 0, 'allindicators'] = 'Gold+' # Stocks that had Golden Cross Potential today
#filter.loc[filter['allindicators'] == 1, 'allindicators'] = 'Gold+' # Stocks that have Golden Cross Potential 1 day prior
filter = filter[['Price','Total', '%Change','Rockets','Recommend', 'allindicators']] # Only show key parameters in final table

# Output results to html table
if not os.path.exists('Filtered-Results'):
    os.makedirs('Filtered-Results')
output = today.strftime("Filtered-Results/%m-%d-%Y_filtered.html")
filter.to_html(output)

# Print results in terminal window
print(filter)
print("\n")
filtered = len(filter)
print("Approved Stocks:   " + str(filtered))
print("Filtered Stocks:   " + str(total - filtered))
print("Total Assessed:    " + str(total))
