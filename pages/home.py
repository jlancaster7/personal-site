import dash
from dash import html

dash.register_page(__name__, path="/", name="Home", title="Home", order=0)

layout = html.Div(
    [
        html.Div(
            html.Div(
                children=[html.H1("Josh's Equity Testing Grounds")],
            )
        )
    ]
)
