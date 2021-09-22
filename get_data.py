from binance.client import Client
from datetime import datetime as dt
import pandas as pd
import sys
import argparse
from tabulate import tabulate
from decouple import config
import yfinance as yf

# import API keys from .env
API_KEY_B = config('API_KEY_B')
SECRET_KEY_B = config('SECRET_KEY_B')

#Use argparse to optimize the data input from the command line
parser = argparse.ArgumentParser(description='Script para generar CSVs de una lista de valores de cryptos en un timeframe definido')
parser.add_argument('--crypto', '-c', help='pide una lista de cryptos, ej: "[\'BTCUSDT\',\'ADAUSDT\']"')
parser.add_argument('--stocks', '-s', help='pide una stock')
#parser.add_argument('--history', '-i', help='toda la data almacenada del to')
parser.add_argument('--timeframe', '-t', default='1d', help='TimeFrame del Query, solo acepta 1h ,4h y 1d', type=str)
parser.add_argument('--startdate', '-st', default='2017-01-01', help='Start date of the query', type=str)
parser.add_argument('--enddate', '-et', default='2021-09-19', help='End date of the query', type=str)

def binance_price_to_csv(ticker):
    """This function stablish a connection to binance, get the historial data from
         3 posibles timeframes,
    """
    client = Client(api_key=API_KEY_B,api_secret=SECRET_KEY_B)
    if time_interval == '4h':
        candles = client.get_klines(symbol=str(ticker), interval=Client.KLINE_INTERVAL_4HOUR, limit=1000)
        candles_data_frame = pd.DataFrame(candles)
        csv = 'crypto_4h.csv'
    if time_interval == '1h':
        candles = client.get_klines(symbol=str(ticker), interval=Client.KLINE_INTERVAL_1HOUR, limit=1000)
        candles_data_frame = pd.DataFrame(candles)
        csv = 'crypto_1h.csv'
    if time_interval == '1d':
        candles = client.get_klines(symbol=str(ticker), interval=Client.KLINE_INTERVAL_1DAY, limit=1000)
        candles_data_frame = pd.DataFrame(candles)
        csv = 'crypto_1d.csv'

    candles_data_frame_date = candles_data_frame[0]/1000
    candles_data_frame_date = (pd.to_datetime(candles_data_frame_date, unit='s'))#.dt.date
    candles_data_frame_date = pd.DataFrame(candles_data_frame_date)
    candles_data_frame_date.columns = ['date']
    final_dataframe = candles_data_frame.join(candles_data_frame_date)
    final_dataframe.drop(final_dataframe.columns[11], axis=1, inplace=True)
    final_dataframe.drop(final_dataframe.columns[0], axis=1, inplace=True)
    final_dataframe.set_index('date', inplace=True)
    final_dataframe.columns=['open', 'high', 'low', 'close', 'volume', 'close_time', 'asset_volume', 
                            'trade_number', 'taker_buy_base', 'taker_buy_quote']
    final_dataframe['change'] = 100*((final_dataframe['close'].astype(float)-final_dataframe['open'].astype(float))/
                            final_dataframe['open'].astype(float))
    final_dataframe.reset_index(inplace=True)
    return final_dataframe, csv

def yfinance_hist(ticker):
    stock = yf.Ticker(ticker)
    hist_stock = stock.history(period='max')
    hist_stock.reset_index(inplace=True)
    hist_stock['name'] = ticker
    csv_n = ticker + '.csv'
    csv = hist_stock.to_csv(csv_n)
    return hist_stock, csv

if __name__== "__main__":
    args = parser.parse_args()
    if args.crypto:
        cryptos = args.crypto.replace('[', ' ').replace(']', ' ').replace(',', ' ').replace("'",'').split()
        time_interval = args.timeframe
        for j,i in enumerate(cryptos):
            crypto_item = binance_price_to_csv(i)[0]
            crypto_item['name'] = i
            csv_name = binance_price_to_csv(i)[1]
            if j == 0:
                df = crypto_item
            elif j==1:
                df_final=pd.concat([df,crypto_item])
            else:
                df_final=pd.concat([df_final,crypto_item])
            print('-'*65)
            print('{0:28}{1:7s}{0:27}'.format('*'*29,i,'*'*26))
            print('-'*65)
            print(tabulate(crypto_item.iloc[:4,:-6],headers=crypto_item.columns, tablefmt='psql', showindex=False, numalign='center', floatfmt='.4f'))
        if len(cryptos) == 1:
            df.to_csv(csv_name, index=False)
        else: 
            df_final.to_csv(csv_name, index=False)
    elif args.stocks:
        st = args.stocks.replace('[','').replace(']','').replace("'",'')
        st1, csv = yfinance_hist(st)
        print(tabulate(st1.head(), headers=st1.columns, tablefmt='psql', showindex=False, numalign='center', floatfmt='.4f'))
        st1.to_csv(csv, index=False)
    else:
        print('En caso de tener problemas usa el parametro "-h" para obtener ayuda')