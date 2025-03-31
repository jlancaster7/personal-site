import dash
from dash import html, dcc
from datetime import datetime, timedelta

from callbacks.fama_french import register_callbacks, page_prefix
import dash_bootstrap_components as dbc

# from components.base_card import base_card
# from components.tables.portfolio import generate_user_portfolio_table

dash.register_page(
    __name__,
    path="/f-f-portfolio",
    name="Fama French Portfolio",
    title="Fama French Portfolio",
    order=2,
)
ticker_field = [
    html.Label("Enter Ticker Symbols:"),
    dcc.Input(
        id=page_prefix + "ticker-input",
        type="text",
        placeholder="Enter tickers separated by commas",
        style={"width": "50%"},
    ),
]
ticker_weights_field = [
    html.Label("Enter Weights for each Ticker:"),
    dcc.Input(
        id=page_prefix + "weights-input",
        type="text",
        placeholder="Enter weights, as decimals, separated by commas",
        style={"width": "50%"},
    ),
]

model_field = [
    html.Label("Select which model to use:"),
    dcc.Dropdown(
        id=page_prefix + "model-dropdown",
        options=[
            {"label": str(i), "value": i}
            for i in [
                # 'CAPM',
                "FF3",
                "FF5",
            ]
        ],
        value="FF3",
        clearable=False,
        # multi=False,
        style={"width": "50%"},
    ),
]

date_picker_field = [
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id=page_prefix + "date-picker",
        start_date=(datetime.now() - timedelta(days=365 * 3)).strftime("%Y-%m-%d"),
        end_date=(datetime.now()).strftime("%Y-%m-%d"),
        display_format="YYYY-MM-DD",
    ),
]
submit = [html.Button("Submit", id=page_prefix + "submit-button")]

register_callbacks()


def layout():
    return dbc.Container(
        children=[
            html.H1("Fama French Portfolio Analysis"),
            dbc.Row([dbc.Col(ticker_field)]),
            dbc.Row([dbc.Col(ticker_weights_field)]),
            dbc.Row([dbc.Col(model_field)]),
            dbc.Row([dbc.Col(date_picker_field)]),
            dbc.Row([dbc.Col(submit)]),
            dbc.Row(
                style={
                    "display": "grid",
                    "gridAutoFlow": "column",
                    "gridTemplateColumns": "100%",
                    "minHeight": "300px",
                },
                children=[
                    dbc.Spinner(
                        children=html.Pre(
                            id=page_prefix + "text-output-pre", children=""
                        ),
                        color="primary",
                        type="border",
                        spinner_style={
                            "width": "3rem",
                            "height": "3rem",
                        },
                    ),
                ],
            ),
        ]
    )
