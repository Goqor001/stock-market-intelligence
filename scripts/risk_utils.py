def calculate_risk_levels(entry_price, rolling_avg_range_pct, multiplier=1.0, rr_value=2.0):
    risk_distance = (
        entry_price
        * rolling_avg_range_pct
        / 100
        * multiplier
    )

    risk_distance = round(risk_distance, 2)
    stop_loss = round(entry_price - risk_distance, 2)
    take_profit = round(entry_price + (rr_value * risk_distance),2)

    return {
        "risk_distance": risk_distance,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "rr": f"1:{int(rr_value)}"
    }