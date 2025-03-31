import dash
from dash import html, dcc


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
                        dcc.Link("Go to PCA", href="/pca", style={"display": "block"}),
                        dcc.Link(
                            "Go to Factor Analysis",
                            href="/f-f-portfolio",
                            style={"display": "block"},
                        ),
                    ],
                ),
            ],
        )
    ]
)
