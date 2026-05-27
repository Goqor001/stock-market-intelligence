import pandas as pd
import sqlite3
from datetime import datetime
from risk_utils import calculate_risk_levels

PENDING_SIGNALS_PATH = "outputs/csv/pending_signals.csv"
ACTIVE_TRADES_PATH = "outputs/csv/active_trades.csv"
DB_PATH = "database/market.db"
SUMMARY_PATH = "outputs/csv/trade_result_summary.csv"

def load_pending_signals():
    pending_df = pd.read_csv(PENDING_SIGNALS_PATH)
    
    return pending_df

def load_prices():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        symbol,
        date,
        open,
        high,
        low,
        close,
        volume
    FROM prices
    ORDER BY symbol, date
    """

    prices_df = pd.read_sql_query(query, conn)

    conn.close()

    return prices_df

def add_volatility_features(prices_df):
    prices_df["daily_range_pct"] = (
        (prices_df["high"] - prices_df["low"])
        / prices_df["close"]
        * 100
    ).round(2)

    window = 14

    prices_df["rolling_avg_range_pct"] = (
        prices_df
        .groupby("symbol")["daily_range_pct"]
        .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
    ).round(2)

    return prices_df

def load_recommended_n():
    summary_df = pd.read_csv(SUMMARY_PATH)

    recommended_n = summary_df["recomended_n"].iloc[0]

    return recommended_n

def create_active_trades(pending_df, prices_df, recommended_n):
    active_trades = []

    for _, signal_row in pending_df.iterrows():
        symbol = signal_row["symbol"]
        signal_date = signal_row["signal_date"]

        future_prices = prices_df[
            (prices_df["symbol"] == symbol) &
            (prices_df["date"] > signal_date)
        ]

        if future_prices.empty:
            continue

        entry_candle = future_prices.iloc[0]

        entry_date = entry_candle["date"]
        entry_price = entry_candle["open"]

        rolling_avg_range_pct = entry_candle["rolling_avg_range_pct"]

        risk = calculate_risk_levels(
            entry_price,
            rolling_avg_range_pct
        )

        trade = {
            "symbol": symbol,
            "signal_date": signal_date,
            "signal": signal_row["signal"],
            "action": "BUY",
            "entry_date": entry_date,
            "entry_price": entry_price,
            "risk_distance": risk["risk_distance"],
            "stop_loss": risk["stop_loss"],
            "take_profit": risk["take_profit"],
            "rr": risk["rr"],
            'recommended_n': recommended_n,
            "status": "ACTIVE",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        active_trades.append(trade)
    
    return pd.DataFrame(active_trades)

def save_active_trades(active_df):
    active_df.to_csv(ACTIVE_TRADES_PATH, index=False)

    print("Active trades saved")

if __name__ == "__main__":
    pending_df = load_pending_signals()

    prices_df = load_prices()

    prices_df = add_volatility_features(prices_df)

    recommended_n = load_recommended_n()

    active_df = create_active_trades(pending_df,prices_df,recommended_n)

    save_active_trades(active_df)
