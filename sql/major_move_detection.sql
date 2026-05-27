WITH t1 AS (
    SELECT
        symbol,
        date,
        open,
        high,
        low,
        close,
        volume
    FROM prices
),
t2 AS (
    SELECT
        *,
        CASE
            WHEN close > open THEN 'bullish_candle'
            WHEN close < open THEN 'bearish_candle'
        END AS candle_direction,
        Round(ABS(close-open),2) AS body_size,
        ROUND(high-low,2) AS candle_range,
        ROUND(AVG(close) OVER(
            PARTITION BY symbol
            ORDER BY date
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ),2) AS rolling_avg_close
    FROM t1
),
t3 AS (
    SELECT
        *,
        ROUND((body_size / candle_range),2) AS body_strength,
        ROUND((close-rolling_avg_close) * 100.0 / rolling_avg_close,2) AS distance_from_avg,
        ROUND(AVG(body_size) OVER(
            PARTITION BY symbol
            ORDER BY date
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ),2) AS rolling_avg_body_size,
        ROUND(AVG(volume) OVER(
            PARTITION BY symbol
            ORDER BY date
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ),0) AS rolling_avg_volume,
        CASE
            WHEN close > rolling_avg_close THEN 'bullish_trend'
            WHEN close < rolling_avg_close THEN 'bearish_trend'
            ELSE 'sideways_trend'
        END AS trend_direction
    FROM t2
),
t4 AS (
    SELECT
        *,
        CASE
            WHEN trend_direction = 'bullish_trend' AND candle_direction = 'bullish_candle' AND body_size > rolling_avg_body_size * 1.5 AND 
                volume > rolling_avg_volume AND body_strength > 0.6 AND distance_from_avg > 1.5 THEN 'strong_bullish_move'
            -- WHEN trend_direction = 'bearish_trend' AND candle_direction = 'bearish_candle' AND body_size > rolling_avg_body_size * 1.5 AND
            --     volume > rolling_avg_volume AND body_strength > 0.6 AND distance_from_avg < -1.5 THEN 'strong_bearish_move'
            ELSE 'normal'
        END AS signal
    FROM t3
)

SELECT *
FROM t4
ORDER BY symbol, date