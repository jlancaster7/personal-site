import dash
from dash import html, dcc
from datetime import datetime, timedelta

from callbacks.pca import register_callbacks
import dash_bootstrap_components as dbc

# from components.base_card import base_card
# from components.tables.portfolio import generate_user_portfolio_table

dash.register_page(__name__, path="/pca", name="PCA", title="PCA", order=1)

ticker_field = [
    html.Label("Enter Ticker Symbols:"),
    dcc.Input(
        id="ticker-input",
        type="text",
        placeholder="Enter tickers separated by commas",
        style={"width": "50%"},
    ),
]
components_field = [
    html.Label("Select Number of Components:"),
    dcc.Dropdown(
        id="components-dropdown",
        options=[{"label": str(i), "value": i} for i in range(1, 6)],
        value=2,
        # multi=False,
        style={"width": "50%"},
    ),
]
date_picker_field = [
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id="date-picker",
        start_date=(datetime.now() - timedelta(days=365 * 3)).strftime("%Y-%m-%d"),
        end_date=(datetime.now()).strftime("%Y-%m-%d"),
        display_format="YYYY-MM-DD",
    ),
]
submit = [html.Button("Submit", id="submit-button")]
register_callbacks()


def layout():

    return dbc.Container(
        [
            html.H1("PCA Analysis of Stock Returns"),
            dbc.Row([dbc.Col(ticker_field)]),
            dbc.Row([dbc.Col(components_field)]),
            dbc.Row([dbc.Col(date_picker_field)]),
            dbc.Row([dbc.Col(submit)]),
            dbc.Row(
                style={
                    "display": "grid",
                    "gridAutoFlow": "column",
                    "gridTemplateColumns": "33% 33% 33%",
                },
                children=[
                    dbc.Col([dcc.Graph(id="bar-chart")], width=4),
                    dbc.Col([dcc.Graph(id="line-plot")], width=4),
                    dbc.Col([dcc.Graph(id="scatter-plot")], width=4),
                ],
            ),
        ]
    )
