[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://warehouse-camo.ingress.cmh1.psfhosted.org/233dfe54c23e0214e7101212ee41d8538f5b4884/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f646a616e676f2e737667)

# Stock Anaylzer
This is a stock analyzing passion project of mine that is in the very early stages. Popular stocks are screended from Reddit using  **AutoDD Rev2** and then I perform technical analysis to filter the list down even further and look for promising buying opportunities. The final table that is producded shows stocks that could be good buying opportunies, with the top stocks on the list indicating a potential upcomming [Golden Cross](https://www.investopedia.com/terms/g/goldencross.asp).

The table produced is sorted in the following order: 

* Potential Golden Cross based on MACD
* How many days all 3 indicators have been met, high to low (RSI > 50, Stochasitcs over 50, MACD Golden Cross passed)
* Slope of the 12 Day average  MACD slope (A larger slope indicates more potential buying momentum with the stock)


From the table, I then manually perform due dilligence of stocks that I could buy options on and apply the [Wheel Strategy](https://www.youtube.com/watch?v=EcsErh9Airs), starting with stocks that have a potential upcoming golden cross.  


Eventually I want to turn this into a Wheel Strategy trading bot similar to [thetagang](https://github.com/brndnmtthws/thetagang). 


## Setup

To install necessary python3 dependencies using pip, run **./setup/install_requriements.sh**.

## Running the Program

To screen reddit and download the historical stock data run (this can take >10 minutes but only needs to be run once a day, time for a coffee break):

```
./screener.sh
```

To filter the screened reddit stocks for possible buying opportunities and export a nicely formatted table run:
```
python3 analyze.py
```

To plot a ticker and investigate the indicators visually (this is a rough visualation, I'd reccomend using [Yahoo Finance](https://finance.yahoo.com/) or [Trading View](https://www.tradingview.com/) instead) run:
```
python3 plot.py --ticker [TICKER] --days [DAYS]

```

## Development
* Rank Stocks by profit probability using historical data instead of the current rankings. 


## Authors

* **Tristan Schuler**

## Acknowledgments

Hat Tip to [u/kaito1410](https://github.com/kaito1410), who developed [AutoDD Rev2](https://github.com/kaito1410/AutoDD_Rev2) which scrapes reddit for the most discussed stocks. **AutoDD Rev2** was slightly modified to work with **StockAnalyzer** as an initial screener from popular reddit stocks. **AutoDD Rev2** is included within **StockAnalyzer**.


