import requests
import pandas as pd

def fetch_stock_data(symbol):

    url = f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol={symbol}&apikey=QnG85MxCSL5syTjabIZbqOoNqmXHzzQm"

    response = requests.get(url)

    data = response.json()

    df = pd.DataFrame(data)

    df.to_csv(f"data/raw/{symbol.lower()}_prices.csv",index=False)

symbols = ["AAPL","MSFT","NVDA","TSLA"]

for symbol in symbols:
    fetch_stock_data(symbol)
