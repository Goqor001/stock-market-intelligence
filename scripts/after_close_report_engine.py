import pandas as pd
from datetime import datetime

PENDING_SIGNALS_PATH = "outputs/csv/pending_signals.csv"
REPORT_PATH = "outputs/reports/after_close_report.txt"

def load_pending_signals():
    pending_df = pd.read_csv(PENDING_SIGNALS_PATH)
    
    return pending_df

def generate_after_close_report(pending_df):
    report = ""

    report += "=== AFTER CLOSE SIGNAL REPORT ===\n\n"
    report += f"Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n"

    if pending_df.empty:
        report += "No pending signals today.\n"
    else:
        report += "=== PENDING SIGNALS ===\n"

        for _,row in pending_df.iterrows():
            report += f"- {row["symbol"]} | {row["signal"]}\n"
            report += f" Action: {row["action"]}\n"
            report += f" Status: {row["status"]}\n"
            report += f" Signal Date: {row["signal_date"]}\n"
            report += " Entry: next market open\n\n"

    return report

def save_report(report):
    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(report)
    
    print("After-close report saved.")

if __name__ == "__main__":
    pending_df = load_pending_signals()
    report = generate_after_close_report(pending_df)
    save_report(report)