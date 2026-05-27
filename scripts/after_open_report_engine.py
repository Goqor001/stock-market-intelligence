import pandas as pd
from datetime import datetime

ACTIVE_TRADE_PATH = "outputs/csv/active_trades.csv"
REPORT_PATH = "outputs/reports/after_open_report.txt"

def load_active_trades():
    active_df = pd.read_csv(ACTIVE_TRADE_PATH)

    return active_df

def generate_after_open_report(active_df):
    report = ""

    report += "=== AFTER OPEN ENTRY REPORT ===\n\n"
    report += f"Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n"

    if active_df.empty:
        report += "No active trades confirmed.\n"
    else:
        report += "=== ENTRY CONFIRMED ===\n"

        for _, row in active_df.iterrows():
            report += f"-- {row["symbol"]} | {row["signal"]}\n"
            report += f"  Action: {row["action"]}\n"
            report += f"  Status: {row["status"]}\n"
            report += f"  Signal Date: {row["signal_date"]}\n"
            report += f"  Entry Date: {row["entry_date"]}\n"
            report += f"  Entry Price: {row["entry_price"]}\n"
            report += f"  Stop Loss: {row["stop_loss"]}\n"
            report += f"  Take_profit {row["take_profit"]}\n"
            report += f"  RR: {row["rr"]}\n"
            report += f"  Recommended Holding: {row["recommended_n"]} days\n\n"

    return report

def save_report(report):
    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(report)
    
    print("After-open report saved.")

if __name__ == "__main__":
    active_df = load_active_trades()
    report = generate_after_open_report(active_df)
    save_report(report)