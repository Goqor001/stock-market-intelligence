import subprocess
import os

print("Step 1: Fetching stock data...")
subprocess.run(["python", "scripts/fetch_stoch_data.py"])

print("Step 2: Saving data to SQLite...")
subprocess.run(["python", "scripts/save_to_db.py"])

print("Step 3: Generating signals...")
subprocess.run(["python", "scripts/signal_engine.py"])

print("Step 4: Creating pending signals...")
subprocess.run(["python", "scripts/pending_signal_engine.py"])

print("Step 5: Generating after-close report...")
subprocess.run(["python", "scripts/after_close_report_engine.py"])

print("Step 6: Sending Telegram report...")
subprocess.run(["python","scripts/telegram_bot.py","outputs/reports/after_close_report.txt"])

print("After-close pipeline completed")