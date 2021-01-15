import pandas as pd
import downloadstocks
from datetime import date

today = date.today()
filename = today.strftime("redditscreens/%m-%d-%Y_redditscreen")

pd.set_option("display.max_rows", None)

df = pd.read_csv(filename + '.csv', index_col = 'Code')

# Intially filter out penny stocks and stocks over $100.  (I don't have that kind of money for buying options... YET)
df = df[df.Price > 5]
df = df[df.Price < 100]
df = df[df.Volume > 500000]


df = df.sort_values(['Code'] , ascending=[True])
filter = df[['Price','Total', '%Change','Rockets','Recommend']]
tickers = filter.index.tolist()
print(filter)

# Download historical data from reddit screened stocks that meet initial filter criteria
downloadstocks.downloadstocks(tickers)
