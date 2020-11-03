import time
import yfinance as yf



class Download_data:
    def __init__(self, history, ticker, extension):
        self._history = history
        self._ticker = ticker
        self._extension = extension

    # Egentlig utdatert metode
    def hent_tickers(self):
        tickers = []
        file = open(self._filename)
        for line in file:
            tickers.append(line.strip())
        file.close()
        return tickers

    # Returns a dataframe of
    def download(self):
        data = ''

        tick = yf.Ticker(f'{self._ticker.upper()}{self._extension}')
        df = tick.history(period=self._history)[['Close', 'Volume']]
        df['TICKER'] = self._ticker
        csv_string = df.to_csv()
        return csv_string
