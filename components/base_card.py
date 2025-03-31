from typing import Any
from dash import html


def base_card(id: str, card_style: dict[str, Any] = {}, children: Any = None):
    return html.Div(
        id=id,
        style={
            "borderRadius": "10px",
            "border": "medium none",
            "box-shadow": "0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24)",
            "padding": "20px",
            "marginTop": "20px",
            "marginBottom": "20px",
            "border-width": "0px 0px 0px 0px",
            "border-style": "solid",
            "border-color": "#e2e2e2",
            "outline-width": "0px",
            "outline-style": "solid",
            "outline-color": "#e2e2e2",
            "background-color": "#f9f9f9",
            **card_style,
        },
        children=children,
    )
