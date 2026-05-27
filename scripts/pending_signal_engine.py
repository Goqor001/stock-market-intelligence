import pandas as pd
import datetime as datetime

SIGNALS_PATH = "outputs/csv/signals.csv"
PENDING_SIGNALS_PATH = "outputs/csv/pending_signals.csv"

def load_signals():
    signals_df = pd.read_csv(SIGNALS_PATH)
    
    return signals_df

def get_latest_actionable_signals(signals_df):
    trade_signals = signals_df[signals_df["signal"] == "strong_bullish_move"].copy()

    latest_date = trade_signals["date"].max()

    latest_signals = trade_signals[trade_signals["date"] == latest_date].copy()

    return latest_signals

def create_pending_signals(latest_signals):
    pending_df = pd.DataFrame()

    pending_df["symbol"] = latest_signals["symbol"]
    pending_df["signal_date"] = latest_signals["date"]
    pending_df["signal"] = latest_signals["signal"]
    pending_df["action"] = "BUY_WATCH"
    pending_df["status"] = "PENDING_ENTRY"
    pending_df["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return pending_df

def save_pending_signals(pending_df):
    pending_df.to_csv(PENDING_SIGNALS_PATH,index=False)

if __name__ == "__main__":
    signals_df = load_signals()

    latest_signals = get_latest_actionable_signals(signals_df)

    pending_df = create_pending_signals(latest_signals)

    save_pending_signals(pending_df)