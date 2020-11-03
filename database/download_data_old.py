import requests
import time
import yfinance as yf


# Getting all tickers
tickers = []
file = open("tickers.txt")
for line in file:
    tickers.append(line.strip())
file.close()






# Downloading stock data and writing to file.
for ticker in tickers:
    tick = yf.Ticker(f"{ticker.upper()}.OL")
    tick.history(period="5y")[["Close", "Volume"]].to_csv(f"data/{ticker}.csv")

    print(f"Downloaded data for: {ticker}...")
    time.sleep(3)


print("Download Complete.")
