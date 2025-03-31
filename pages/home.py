import dash
from dash import html

from components.base_card import base_card

dash.register_page(__name__, path="/", name="Home", title="Home", order=0)

layout = html.Div(
    [
        base_card(
            id="home-card",
            children=[
                html.H2("Welcome to my site!"),
                html.P(
                    "This is the home page of the Dash app where you can find links to various analyses."
                ),
                html.P("You can navigate to the following pages:"),
                html.Div(
                    style={
                        "display": "grid",
                        "gridAutoFlow": "row",
                        "rowGap": "10px",
                    },
                    children=[
                        html.A("Go to PCA", href="/pca", className="btn btn-primary"),
                        html.A(
                            children="Go to Fama French Regression",
                            # children=html.Button("Go to Fama French Regression"),
                            href="/f-f-portfolio",
                            className="btn btn-secondary",
                        ),
                    ],
                ),
            ],
        )
    ]
)
