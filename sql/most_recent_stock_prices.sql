SELECT date, ticker, value
FROM finance__economics.cybersyn.stock_price_timeseries
WHERE ticker IN {ticker_list}
  AND variable_name = 'Post-Market Close'
QUALIFY ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) = 1;