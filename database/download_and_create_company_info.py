import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from datetime import datetime
from progress.bar import IncrementalBar
import sqlite3

databaseName = 'database.sqlite3'


# Downloads company description from Yahoo Finance
def get_description(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}.OL/profile?p={ticker}.OL'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    t = soup.findAll('p', {'class': 'Mt(15px) Lh(1.6)'})
    try:
        p = ''.join(t[0].findAll(text=True))
        return p
    except Exception as e:
        file = open('download_description_log.txt', 'a')
        file.write(f'get_description() failed on \"{ticker}\": Error: \"{e}\" \n')
        file.close()

        file = open('missing_description.txt', 'a')
        file.write(ticker)
        file.close()
        return False

'''
for node in t:
    print(''.join(node.findAll(text=True)))
'''


def add_description_to_database(ticker, description):
    conn = sqlite3.connect(databaseName)

    this_date = datetime.today().strftime('%Y-%m-%d')

    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO companyDescription(ticker, description, date_added)
            VALUES(?, ?, ?)
        ''', (ticker, description, this_date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        print(f'Exception Raised: {e}')
        conn.close()
        return False




def create_table():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS companyDescription(
        id INTEGER PRIMARY KEY,
        ticker TEXT,
        description TEXT,
        date_added INTEGER
        )
    ''')

def get_tickers():
    tickers = []
    for line in open('tickers.txt'):
        tickers.append(line.strip())
    return tickers




def main():
    tickers = get_tickers()
    bar = IncrementalBar('Countdown', max=len(tickers))
    for ticker in tickers:
        description = get_description(ticker)
        if description:
            if add_description_to_database(ticker, description):
                pass
            else:
                print(f'Error on {ticker}.')
        bar.next()
        time.sleep(14)

    print('Download Complete!')





create_table()
main()





















#
