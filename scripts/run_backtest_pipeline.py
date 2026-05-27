import subprocess

print("Step 1: Fetching stock data...")
subprocess.run(["python","scripts/fetch_stock_data.py"])

print("Step 2: Saving data to SQLite...")
subprocess.run(["python","scripts/save_to_db.py"])

print("Step 3: Generating signals...")
subprocess.run(["python","scripts/signal_engine.py"])

print("Step 4: Adding risk levels...")
subprocess.run(["python","scripts/risk_engine.py"])

print("Step 5: Backtest signal...")
subprocess.run(["python","scripts/backtest_engine.py"])

print("Step 6: Generate market report...")
subprocess.run(["python","scripts/report_engine.py"])

print("Pipeline completed successfully.")