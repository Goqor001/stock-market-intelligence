import pandas as pd
import datetime

SIGNALS_PATH = "outputs/csv/signals_with_risk.csv"
SUMMARY_PATH = "outputs/csv/trade_result_summary.csv"
REPORT_PATH = "outputs/reports/daily_market_report.txt"

def load_signals():
    df = pd.read_csv(SIGNALS_PATH)

    return df

def load_summary():
    df = pd.read_csv(SUMMARY_PATH)

    return df

def get_latest_signals(signals_df):
    latest_date = signals_df["date"].max()

    latest_signals = signals_df[signals_df["date"]==latest_date]

    return latest_signals

def get_recomended_metrics(summary_df):
    recommended_n = summary_df["best_n_by_total_return"].iloc[0]

    recommended_metrics = summary_df[summary_df["n_days"] == recommended_n]

    return recommended_metrics.iloc[0]

def generate_report(latest_signals, recommended_metrics):
    report = ""

    report += "=== DAILY MARKET REPORT ===\n\n"
    report += f"Generated at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n"

    report += "=== STRATEGY SUMMARY ===\n"
    report += f"Recommended N: {recommended_metrics["n_days"]} days\n"
    report += f"Winrate: {recommended_metrics["winrate"]}%\n"
    report += f"Avg Return: {recommended_metrics["avg_return"]}%\n"
    report += f"Total Return: {recommended_metrics["total_return"]}%\n\n"
    
    report += "=== LATEST SIGNALS ===\n"

    if latest_signals.empty:
        report += "No latest actionablesignals.\n"
    else:
        for _,row in latest_signals.iterrows():
            report += f"- {row["symbol"]} | {row["signal"]}\n"

            if row["signal"] == "strong_bullish_move":
                action = "BUY"
                confidence = "HIGH"
            else:
                action = "WATCH"
                confidence = "MEDIUM"

            report += f" Action: {action}\n"
            report += f" Confidence: {confidence}\n"

            report += f" Signal Date: {row["date"]}\n"
            report += f" Entry Date: {row["entry_date"]}\n"
            report += f" Entry Price: {row["entry_price"]}\n"
            report += f" Stop Loss: {row["stop_loss"]}\n"
            report += f" Take Profit: {row["take_profit"]}\n"
            report += f" Recommended Holding: {recommended_metrics["n_days"]} days\n\n"

    return report

def save_report(report):
    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(report)
    
    print("Daily market report generated.")

if __name__ == "__main__":
    signals_df = load_signals()
    summary_df =load_summary()

    latest_signals = get_latest_signals(signals_df)

    recommended_metrics = get_recomended_metrics(summary_df)

    report = generate_report(latest_signals,recommended_metrics)

    save_report(report)