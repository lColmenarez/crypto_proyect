-- Create DBs for Stocks and Crypto
postgres=# CREATE DATABASE stocks;
postgres=# CREATE DATABASE crypto;

-- Creatinfg tables inside the stocks.db
-- primary table (holds the company data)
CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY, 
    symbol TEXT NOT NULL UNIQUE, 
    company TEXT NOT NULL
);

--Secundary table golds de ohlc data + dividends + splits
CREATE TABLE IF NOT EXISTS stock_price (
    id INTEGER PRIMARY KEY, 
    stock_id INTEGER,
    date_ DATE NOT NULL,
    open_ FLOAT NOT NULL, 
    high FLOAT NOT NULL, 
    low FLOAT NOT NULL, 
    close_ FLOAT NOT NULL, 
    dividends FLOAT NOT NULL,
    stocks_splits TEXT NOT NULL,
    volume INT NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock (id)
);