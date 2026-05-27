import pandas as pd
import sqlite3

def generate_signals():
    conn = sqlite3.connect("database/market.db")

    with open("sql/major_move_detection.sql","r") as file:
        query = file.read()
    
    signals_df = pd.read_sql(query, conn)

    signals_df.to_csv("outputs/csv/signals.csv", index=False)

    conn.close()

    print("Signals saved to outputs/csv/signals.csv")


generate_signals()