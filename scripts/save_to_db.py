import pandas as pd
import sqlite3

symbols = ["AAPL","MSFT","NVDA","TSLA"]

conn = sqlite3.connect("database/market.db")

conn.execute("DROP TABLE IF EXISTS prices")

for symbol in symbols:
    file_path = f"data/raw/{symbol.lower()}_prices.csv"

    df = pd.read_csv(file_path)

    if "symbol" not in df.columns:
        df["symbol"] = symbol
    
    df.to_sql("prices", conn, if_exists="append", index=False)

    print(symbol, "saved to SQLite")

conn.close()
