import subprocess

print("Step 1: Processing pending entries...")
subprocess.run(["python","scripts/entry_engine.py"])

print("Step 2: Generating after-open report...")
subprocess.run(["python","scripts/after_open_report_engine.py"])

print("Step 3: Sending Telegram report...")
subprocess.run(["python","scripts/telegram_bot.py","outputs/reports/after_open_report.txt"])