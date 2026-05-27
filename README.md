````markdown id="qwe742"
# Stock Market Intelligence System

Automated multi-asset stock market intelligence system with signal generation, adaptive risk management, backtesting, GitHub Actions automation, and Telegram reporting.

---

# Project Overview

This project is an automated market analysis and signal delivery system designed to:

- collect stock market data
- detect trading signals
- calculate adaptive risk levels
- generate reports
- send Telegram alerts
- run automatically in the cloud using GitHub Actions

The system currently supports multiple assets and includes separate workflows for:

- after market close analysis
- after market open trade confirmation

---

# Features

## Data Pipeline

- Fetch stock market data using Yahoo Finance
- Store historical data in CSV and SQLite
- Multi-asset processing

## Signal Engine

- Detect strong bullish market movements
- Generate actionable trading signals
- Separate pending and confirmed trade logic

## Risk Management

- Adaptive stop loss and take profit calculation
- Volatility-based risk distance
- Risk/reward ratio calculation

## Backtesting

- Historical signal evaluation
- Trade result analysis
- Performance summary generation

## Automation

- GitHub Actions cloud execution
- Scheduled workflows
- Fully automated pipelines

## Telegram Integration

- After-close market alerts
- After-open entry confirmation alerts
- Automated report delivery

---

# Technology Stack

- Python
- pandas
- SQLite
- GitHub Actions
- Telegram Bot API
- requests
- yfinance

---

# Project Structure

```text
stock-market-intelligence/
│
├── .github/workflows/
│   ├── after_close.yml
│   └── after_open.yml
│
├── data/raw/
│   ├── aapl_prices.csv
│   ├── msft_prices.csv
│   ├── nvda_prices.csv
│   └── tsla_prices.csv
│
├── database/
│   └── market.db
│
├── outputs/
│   ├── csv/
│   └── reports/
│
├── scripts/
│   ├── fetch_stock_data.py
│   ├── save_to_db.py
│   ├── signal_engine.py
│   ├── pending_signal_engine.py
│   ├── entry_engine.py
│   ├── risk_engine.py
│   ├── risk_utils.py
│   ├── backtest_engine.py
│   ├── report_engine.py
│   ├── after_close_report_engine.py
│   ├── after_open_report_engine.py
│   ├── telegram_bot.py
│   ├── run_backtest_pipeline.py
│   ├── run_after_close_pipeline.py
│   └── run_after_open_pipeline.py
│
├── sql/
│   └── major_move_detection.sql
│
├── .gitignore
├── README.md
└── requirements.txt
````

---

# System Workflow

## After Market Close Pipeline

Fetch Market Data
→ Save to SQLite
→ Generate Signals
→ Create Pending Signals
→ Generate After-Close Report
→ Send Telegram Alert

### Purpose

* identify new market opportunities
* send BUY_WATCH alerts
* prepare pending trades for next market open

---

## After Market Open Pipeline

Process Pending Signals
→ Confirm Entry Price
→ Calculate Risk Levels
→ Create Active Trades
→ Generate After-Open Report
→ Send Telegram Alert

### Purpose

* confirm real market entries
* calculate adaptive SL/TP
* activate trades after market open

---

# Signal Lifecycle

Signal Detected
→ Pending Entry
→ Entry Confirmed
→ Active Trade

---

# GitHub Actions Automation

The system runs automatically in the cloud using GitHub Actions.

## Automated Workflows

### After Close Pipeline

Runs automatically after market close.

### After Open Pipeline

Runs automatically after market open.

The workflows:

* install dependencies
* execute pipelines
* generate reports
* send Telegram notifications

No local machine is required for execution.

---

# Example Telegram Alerts

## After Close

```text
=== PENDING SIGNALS ===
NVDA | strong_bullish_move
Action: BUY_WATCH
Status: PENDING_ENTRY
Entry: next market open
```

## After Open

```text
=== ENTRY CONFIRMED ===
NVDA | strong_bullish_move
Action: BUY
Status: ACTIVE
Entry Price: 229.76
Stop Loss: 221.97
Take Profit: 245.34
RR: 1:2
```

---

# Future Improvements

Planned future upgrades:

* TP/SL hit tracking
* Trade lifecycle engine
* Portfolio analytics
* Machine learning scoring
* AI-based signal ranking
* Advanced backtesting metrics
* Dashboard visualization
* Cloud database storage

---

# Disclaimer

This project is for educational and research purposes only.

It does not provide financial advice.

All trading decisions and risk management remain the responsibility of the user.

```
```
