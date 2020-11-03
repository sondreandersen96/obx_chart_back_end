import sqlite3
from Download_data import Download_data
from datetime import datetime
from progress.bar import IncrementalBar
import time

start_time = time.time()


databaseName = 'database.sqlite3'


def create_table():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS priceHistory(
        id INTEGER PRIMARY KEY,
        ticker TEXT,
        close REAL,
        date TEXT,
        date_added INTEGER,
        volume INTEGER
        )
        ''')
    conn.commit()
    conn.close()


def get_tickers(filename):
    tickers = []
    file = open(filename)
    for line in file:
        tickers.append(line.strip())
    file.close()
    return tickers


def insert_data(ticker):
    data = Download_data('5y', ticker, '.OL').download()
    conn = sqlite3.connect(databaseName)

    for line in data.split('\n')[1:]: # Must skip first row because it cointains headers
        try:
            security = line.split(',')
            date = security[0]
            close = security[1]
            volume = security[2]
            ticker = security[3]

            this_date = datetime.today().strftime('%Y-%m-%d')

            # Adding to database

            c = conn.cursor()

            c.execute('''
                INSERT INTO priceHistory(date, close, volume, ticker, date_added)
                VALUES(?, ?, ?, ?, ?)''', (date, close, volume, ticker, this_date))

            conn.commit()
            #print(f'Date: {date}, Close: {close}, Volume: {volume}, Ticker: {ticker}')
        except Exception as e:
            conn.rollback()
            if len(line) > 0:
                file = open('download_log.txt', 'a')
                file.write(f'-> Error downloading, line in csv filen START-{line}-END. {e}\n')
                file.close()
    conn.close()





# Creating a new table in database called priceHistory if it doesnt already exist.
create_table()

# Adding data downloaded from Yahoo Finance to database.
tickers = get_tickers('tickers.txt')
bar = IncrementalBar('Countdown', max=len(tickers))
for ticker in tickers:
    bar.next()
    insert_data(ticker)

bar.finish()


#data = Download_data('1y', 'NEL', '.OL').download()

#print(data)

















print(f'Completing this program took: {(time.time() - start_time)} secounds.')
