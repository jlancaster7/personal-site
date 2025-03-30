import dash
from dash import html
from callbacks.portfolio import register_callbacks
from components.base_card import base_card
from components.tables.portfolio import generate_user_portfolio_table

# dash.register_page(
#     __name__, path="/portfolio", name="Portfolio", title="Portfolio", order=1
# )

register_callbacks()

layout = html.Div(
    style={"display": "grid", "columnGap": "10px", "rowGap": "10px"},
    children=[
        html.Div(
            id="portfolio-page-load-callback-initializer", style={"display": "none"}
        ),
        html.Div(
            children=base_card(
                "test-card-1", children=html.H1("Testing Card Component")
            )
        ),
        html.Div(
            style={"height": "400px"},
            children=[
                base_card(
                    id="test-card-2",
                    card_style={"height": "100%"},
                    children=[generate_user_portfolio_table()],
                )
            ],
        ),
    ],
)
