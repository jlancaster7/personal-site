WITH ytd_performance AS (
  SELECT
    ticker,
    MIN(date) OVER (PARTITION BY ticker) AS start_of_year_date,
    FIRST_VALUE(value) OVER (PARTITION BY ticker ORDER BY date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS start_of_year_price,
    MAX(date) OVER (PARTITION BY ticker) AS latest_date,
    LAST_VALUE(value) OVER (PARTITION BY ticker ORDER BY date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS latest_price
  FROM finance__economics.cybersyn.stock_price_timeseries
  WHERE
    ticker IN ('AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA')
    AND date >= DATE_TRUNC('YEAR', CURRENT_DATE()) -- Truncates the current date to the start of the year
    AND variable_name = 'Post-Market Close'
)
SELECT
  ticker,
  start_of_year_date,
  start_of_year_price,
  latest_date,
  latest_price,
  (latest_price - start_of_year_price) / start_of_year_price * 100 AS percentage_change_ytd
FROM
  ytd_performance
GROUP BY
  ticker, start_of_year_date, start_of_year_price, latest_date, latest_price
ORDER BY percentage_change_ytd DESC;