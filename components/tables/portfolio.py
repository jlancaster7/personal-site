from pandas import DataFrame
from components.base_ag_grid import base_ag_grid

portfolio_table_columns = [
    {"field": "ticker", "headerName": "Ticker"},
    {"field": "num_shares", "headerName": "# Shares"},
    {
        "field": "price",
        "headerName": "Last Px",
        "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"},
    },
    {
        "field": "avg_cost",
        "headerName": "Avg Cost",
        "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"},
    },
    {
        "field": "market_value",
        "headerName": "Mkt Value",
        "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"},
    },
    {
        "field": "unrealized_gain_loss",
        "headerName": "Unrlzd G/L",
        "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"},
    },
]


def generate_user_portfolio_table():
    return base_ag_grid(
        id="user-portfolio-table",
        row_data=DataFrame([]),
        column_defs=portfolio_table_columns,
        style={"height": "90%", "border": None},
    )
