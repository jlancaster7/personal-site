from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
    callback,
    set_props,
    page_container,
    page_registry,
)
import os
import traceback
from dotenv import load_dotenv
from utils.utils import Logger
import dash_bootstrap_components as dbc
from openbb import obb


obb.account.login(pat=os.getenv("OPENBB_PERSONAL_ACCESS_TOKEN"), remember_me=True)  # type: ignore
# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
is_heroku = "DYNO" in os.environ  # True if running on Heroku, False if local

if is_heroku:
    # Production environment (Heroku)
    print("Running on Heroku!")
    # Place any Heroku-specific config here
else:
    # Local environment
    load_dotenv()
    print("Running locally.")
    # Place any local development config here


def custom_error_handler(err):
    my_logger = Logger("Custom Dash Error Handler")
    body = f"""
        Error {str(err)}
        Trackback info: {traceback.format_exc()}\n\n
    """
    my_logger.error(body)
    set_props(
        "toast-message",
        dict(
            is_open=True,
            children="An error has occurred. Contact lancaster.joshua.c@gmail.com.",
        ),
    )


app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Testing Grounds",
    on_error=custom_error_handler,
)

server = app.server

app.layout = html.Div(
    style={"backgroundColor": "#f9f9f9"},
    children=[
        html.Div(id="page-load-callback-initializer", style={"display": "none"}),
        html.Div(
            children=[
                html.Div(
                    id="page-header",
                    style={
                        "backgroundColor": "grey",
                        "color": "white",
                        "display": "grid",
                        "gridAutoFlow": "column",
                        "gridTemplateColumns": "50% 50%",
                    },
                )
            ]
        ),
        page_container,
        dbc.Toast(
            id="toast-message",
            header="Input Error",
            duration=4000,
            is_open=False,
            style={
                "position": "fixed",
                "top": 20,
                "left": "50%",
                "transform": "translateX(-50%)",
                "width": "300px",
                "backgroundColor": "#f8d7da",
                "color": "#721c24",
                "border": "1px solid #f5c6cb",
                "borderRadius": "5px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                "padding": "15px",  # Added padding for text
            },
            # dismissable=True,
            header_style={
                "color": "#721c24",
                "fontWeight": "bold",
                "borderBottom": "1px solid #f5c6cb",
                "paddingBottom": "10px",  # Added padding for header
            },
            body_style={
                "paddingTop": "10px",  # Added padding for body text
            },
        ),
    ],
)


@callback(
    Output("page-header", "children"),
    Input("page-load-callback-initializer", "children"),
)
def initialize_header(_):
    return [
        html.Div(
            style={"display": "grid", "gridAutoFlow": "column"},
            children=[
                html.H1(
                    style={
                        "display": "grid",
                        "width": "fit-content",
                        "whitespace": "nowrap",
                        "color": "white",
                        "padding": "8px",
                        "paddingRight": "24px",
                    },
                    children=dcc.Link(
                        href=page["relative_path"], children=f"{page['name']}"
                    ),
                )
                for page in page_registry.values()
            ],
        )
    ]


if __name__ == "__main__":
    if is_heroku:
        app.run(debug=False)
    else:
        app.run(debug=True)
