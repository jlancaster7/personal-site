import dash
from dash import html, dcc
from datetime import datetime, timedelta

from callbacks.pca import register_callbacks, page_prefix
from components.base_card import base_card
import dash_bootstrap_components as dbc

# from components.base_card import base_card
# from components.tables.portfolio import generate_user_portfolio_table

dash.register_page(__name__, path="/pca", name="PCA", title="PCA", order=1)

ticker_field = [
    html.Label("Enter Ticker Symbols:"),
    dcc.Input(
        id=page_prefix + "ticker-input",
        type="text",
        placeholder="Enter tickers separated by commas",
        style={"height": "40px", "width": "300px", "fontSize": "14px"},
        # style={"width": "50%"},
    ),
]
components_field = [
    html.Label("Select Number of Components:"),
    dcc.Dropdown(
        id=page_prefix + "components-dropdown",
        options=[{"label": str(i), "value": i} for i in range(1, 6)],
        value=2,
        clearable=False,
        # multi=False,
        style={"height": "40px", "width": "300px", "fontSize": "14px"},
        # style={"width": "50%"},
    ),
]
date_picker_field = [
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id=page_prefix + "date-picker",
        start_date=(datetime.now() - timedelta(days=365 * 3)).strftime("%Y-%m-%d"),
        end_date=(datetime.now()).strftime("%Y-%m-%d"),
        display_format="YYYY-MM-DD",
        style={"height": "40px", "width": "300px", "fontSize": "14px !important"},
    ),
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
                    html.H1(
                        "PCA Analysis of Stock Returns",
                        style={"marginTop": "0px", "marginBottom": "10px"},
                    ),
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
                                children=ticker_field,
                            ),
                            html.Div(
                                style={
                                    "display": "grid",
                                    "gridAutoFlow": "row",
                                    "alignContent": "space-between",
                                },
                                children=components_field,
                            ),
                            html.Div(
                                style={
                                    "display": "grid",
                                    "gridAutoFlow": "row",
                                    "alignContent": "space-between",
                                },
                                children=date_picker_field,
                            ),
                        ],
                    ),
                    html.Div(children=submit),
                ],
            ),
            base_card(
                id=page_prefix + "inputs-card",
                card_style={
                    "display": "grid",
                    "gridAutoFlow": "column",
                    "gridTemplateColumns": "repeat(3, 1fr)",
                    "columnGap": "10px",
                },
                children=[
                    html.Div(
                        style={
                            "borderRadius": "10px",
                        },
                        children=dcc.Graph(id=page_prefix + "bar-chart"),
                    ),
                    html.Div(
                        style={
                            "borderRadius": "10px",
                        },
                        children=dcc.Graph(id=page_prefix + "line-plot"),
                    ),
                    html.Div(
                        style={
                            "borderRadius": "10px",
                        },
                        children=dcc.Graph(id=page_prefix + "scatter-plot"),
                    ),
                ],
            ),
        ]
    )
