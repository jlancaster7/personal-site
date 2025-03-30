with user_portfolio as (
    SELECT fact_users.user_name
            ,dim_brokers.broker_name
            ,dim_port.portfolio_name
            ,holdings.* 
    FROM michaels_pms.public.fact_investment_portfolio_holdings as holdings
    JOIN michaels_pms.public.dim_investment_portfolios as dim_port
        ON holdings.portfolio_id = dim_port.id
    join michaels_pms.public.dim_brokers as dim_brokers
        on dim_port.broker_id = dim_brokers.id
    join michaels_pms.public.fact_users as fact_users
        on dim_port.user_id = fact_users.id
    where 1=1
    and fact_users.id = 1 -- {user_id}
),
market_data as (
    SELECT date, ticker, value
    FROM finance__economics.cybersyn.stock_price_timeseries
    WHERE ticker IN (select ticker from user_portfolio)
      AND variable_name = 'Post-Market Close'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) = 1
)
select
    port.ticker
    , port.num_shares
    , port.avg_cost
    , market.date as price_date
    , market.value as price
    , port.num_shares * market.value as market_value
    , port.num_shares * port.avg_cost as total_cost
    , (port.num_shares * market.value) - (port.num_shares * port.avg_cost) as unrealized_gain_loss
    , port.user_name
    , port.broker_name
    , port.portfolio_name
    , port.as_of as portfolio_as_of_date
    , port.last_updated as portfolio_last_updated_date
from user_portfolio as port
join market_data as market
    on port.ticker = market.ticker
;