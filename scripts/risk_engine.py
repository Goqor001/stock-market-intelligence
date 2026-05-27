import pandas as pd
from risk_utils import calculate_risk_levels

def add_risk_levels():
    signals = pd.read_csv("outputs/csv/signals.csv")

    signals["daily_range_pct"] = (
        (signals["high"] - signals["low"])
        / signals["close"]
        * 100
    ).round(2)

    window = 14

    signals["rolling_avg_range_pct"] = (
        signals
        .groupby("symbol")["daily_range_pct"]
        .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
    ).round(2)

    signals["entry_price"] = (
    signals
    .groupby("symbol")["open"]
    .shift(-1)
    )   

    signals["entry_date"] = (
        signals
        .groupby("symbol")["date"]
        .shift(-1)
    )

    trade_signals = signals[
        signals["signal"] == "strong_bullish_move"
    ].copy()

    trade_signals = trade_signals.dropna(subset=["entry_price","entry_date"])
    trade_signals["rr"] = "1:2"

    risk_results = trade_signals.apply(
        lambda row: calculate_risk_levels(
            row["entry_price"],
            row['rolling_avg_range_pct']
        ),
        axis=1
    )

    trade_signals["risk_distance"] = risk_results.apply(lambda x: x["risk_distance"])
    trade_signals["stop_loss"] = risk_results.apply(lambda x: x["stop_loss"])
    trade_signals["take_profit"] = risk_results.apply(lambda x: x["take_profit"])
    trade_signals["rr"] = risk_results.apply(lambda x: x["rr"])

    trade_signals.to_csv("outputs/csv/signals_with_risk.csv",index=False)

    print("Signals with risk levels saved")

add_risk_levels()

