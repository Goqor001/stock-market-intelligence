import pandas as pd
import sqlite3

SIGNALS_PATH = "outputs/csv/signals_with_risk.csv"
DB_PATH = "database/market.db"
TRADE_RESULTS_PATH = "outputs/csv/trade_results.csv"
BACKTEST_SUMMARY_PATH = "outputs/csv/trade_result_summary.csv"

N_VALUES = [3,5,7,10,15]

def load_signals():
    df = pd.read_csv(SIGNALS_PATH)
    return df

def load_prices():
    conn = sqlite3.connect("database/market.db")

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

def get_future_candles(prices_df, symbol, entry_date, n_days):
    future_candles = prices_df[
        (prices_df["symbol"] == symbol) &
        (prices_df["date"] > entry_date)
    ].head(n_days)

    return future_candles

def evaluate_trade(signal_row, future_candles):
    stop_loss = signal_row["stop_loss"]
    take_profit = signal_row["take_profit"]

    if future_candles.empty:
        return {
            "outcome": "NO_DATA",
            "exit_date": None,
            "exit_price": None
        }

    for _, candle in future_candles.iterrows():
        hit_sl = candle["low"] <= stop_loss
        hit_tp = candle["high"] >= take_profit

        if hit_sl and hit_tp:
            return {
                "outcome": "SL_HIT",
                "exit_date": candle["date"],
                "exit_price": stop_loss
            }
        
        elif hit_sl:
            return {
                "outcome": "SL_HIT",
                "exit_date": candle["date"],
                "exit_price": stop_loss
            }
        
        elif hit_tp:
            return {
                "outcome": "TP_HIT",
                "exit_date": candle["date"],
                "exit_price": take_profit
            }
    
    last_candle = future_candles.iloc[-1]

    return{
        "outcome": "EXPIRED",
        "exit_date": last_candle["date"],
        "exit_price": last_candle["close"]
    }



def run_backtest_for_n(signals_df, prices_df, n_days):
    results = []
    
    for _, signal_row in signals_df.iterrows():
        symbol = signal_row["symbol"]
        entry_date = signal_row["entry_date"]

        future_candles = get_future_candles(
            prices_df,
            symbol,
            entry_date,
            n_days
        )

        trade_result = evaluate_trade(signal_row, future_candles)

        if trade_result["exit_price"] is not None:
            return_pct = (
                (trade_result["exit_price"] - signal_row["entry_price"])
                / signal_row["entry_price"]
                * 100
            )
        else:
            return_pct = None

        result_row = {
            "symbol": symbol,
            "signal_date": signal_row["date"],
            "entry_date": entry_date,
            "entry_price": signal_row["entry_price"],
            "stop_loss": signal_row["stop_loss"],
            "take_profit": signal_row["take_profit"],
            "n_days": n_days,
            "outcome": trade_result["outcome"],
            "exit_date": trade_result["exit_date"],
            "exit_price": trade_result["exit_price"],
            "return_pct": round(return_pct,2) if return_pct is not None else None
        }

        results.append(result_row)

    return pd.DataFrame(results)

def run_multiple_n_backtest(signals_df, prices_df):
    all_results = []

    for n_days in N_VALUES:
        backtest_results = run_backtest_for_n(
            signals_df,
            prices_df,
            n_days
        )

        all_results.append(backtest_results)
    
    final_results = pd.concat(all_results, ignore_index=True)

    return final_results

def save_results(results_df):
    results_df.to_csv(TRADE_RESULTS_PATH,index=False)

def save_summary(results_df):
    summary = (
        results_df
        .groupby("n_days")
        .agg(
            total_trades=("outcome","count"),
            tp_hits=("outcome",lambda x: (x == "TP_HIT").sum()),
            sl_hits=("outcome",lambda x: (x == "SL_HIT").sum()),
            expired =("outcome", lambda x: (x== "EXPIRED").sum()),
            no_data=("outcome", lambda x: (x == "NO_DATA").sum()),
            avg_return=("return_pct", "mean"),
            median_return=("return_pct","median"),
            total_return=("return_pct","sum")
        )
        .reset_index()
    )
    
    expired_avg_returns = []
    expired_total_returns = []

    for n_days in summary["n_days"]:
        n_df = results_df[results_df["n_days"] == n_days]

        expired_df = n_df[n_df["outcome"] == "EXPIRED"]

        expired_avg_returns.append(expired_df["return_pct"].mean())
        expired_total_returns.append(expired_df["return_pct"].sum())

    summary["expired_avg_return"] = expired_avg_returns
    summary["expired_total_return"] = expired_total_returns

    summary["expired_avg_return"] = summary["expired_avg_return"].round(2)
    summary["expired_total_return"] = summary["expired_total_return"].round(2)

    summary["winrate"] = (
        summary["tp_hits"] / summary["total_trades"] * 100
    ).round(2)
    summary["avg_return"] = summary["avg_return"].round(2)
    summary["median_return"] = summary["median_return"].round(2)
    summary["total_return"] = summary["total_return"].round(2)

    best_n_by_total_return = summary.loc[
        summary["total_return"].idxmax(),
        "n_days"
    ]

    best_n_by_avg_return = summary.loc[
        summary["avg_return"].idxmax(),
        "n_days"
    ]

    summary["best_n_by_total_return"] = best_n_by_total_return
    summary["best_n_by_avg_return"] = best_n_by_avg_return
    summary["recomended_n"] = best_n_by_total_return

    summary.to_csv(BACKTEST_SUMMARY_PATH, index=False)

if __name__ == "__main__":
    signals_df = load_signals()
    prices_df = load_prices()

    results_df = run_multiple_n_backtest(signals_df, prices_df)

    save_results(results_df)

    save_summary(results_df)

    print("Backtest results and summary saved")

