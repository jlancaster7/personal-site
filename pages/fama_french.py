import dash
from dash import html, dcc
from datetime import datetime, timedelta

from callbacks.fama_french import register_callbacks, page_prefix
from components.base_card import base_card
import dash_bootstrap_components as dbc

# from components.base_card import base_card
# from components.tables.portfolio import generate_user_portfolio_table

dash.register_page(
    __name__,
    path="/f-f-portfolio",
    name="Fama French Portfolio Analysis",
    title="Fama French Portfolio Analysis",
    order=2,
)
ticker_field = [
    html.Label("Enter Ticker Symbols:"),
    dcc.Input(
        id=page_prefix + "ticker-input",
        type="text",
        placeholder="Enter tickers separated by commas",
        style={"height": "40px", "width": "300px", "fontSize": "14px"},
    ),
]
ticker_weights_field = [
    html.Label("Enter Weights for each Ticker:"),
    dcc.Input(
        id=page_prefix + "weights-input",
        type="text",
        placeholder="Enter weights, as decimals, separated by commas",
        style={"height": "40px", "width": "300px", "fontSize": "14px"},
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
        style={"height": "40px", "width": "300px", "fontSize": "14px"},
    ),
]

date_picker_field = [
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id=page_prefix + "date-picker",
        start_date=(datetime.now() - timedelta(days=365 * 3)).strftime("%Y-%m-%d"),
        end_date=(datetime.now()).strftime("%Y-%m-%d"),
        display_format="YYYY-MM-DD",
        style={"height": "40px", "width": "300px", "fontSize": "14px"},
    ),
]
field_list = [
    ticker_field,
    ticker_weights_field,
    model_field,
    date_picker_field,
]

submit = [html.Button("Submit", id=page_prefix + "submit-button")]

register_callbacks()


def layout():
    return html.Div(
        children=[
            base_card(
                id=page_prefix + "inputs-card",
                card_style={
                    "display": "grid",
                    "gridAutoFlow": "row",
                    "rowGap": "10px",
                },
                children=[
                    html.H1("Fama French Portfolio Analysis"),
                    html.Div(
                        style={
                            "display": "grid",
                            "gridAutoFlow": "column",
                            "columnGap": "10px",
                        },
                        children=[
                            html.Div(
                                style={
                                    "display": "grid",
                                    "gridAutoFlow": "row",
                                    "alignContent": "space-between",
                                },
                                children=field,
                            )
                            for field in field_list
                        ],
                    ),
                    html.Div(children=submit),
                ],
            ),
            base_card(
                id=page_prefix + "output-card",
                card_style={
                    "display": "grid",
                    "gridAutoFlow": "column",
                    "gridTemplateColumns": "100%",
                    "minHeight": "400px",
                },
                children=[
                    dbc.Spinner(
                        children=html.Pre(
                            id=page_prefix + "text-output-pre",
                            style={"height": "100%"},
                            children="",
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
