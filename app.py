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
from services.snow import SnowflakeConnector
from openbb import obb

load_dotenv()
obb.account.login(pat=os.getenv("OPENBB_PERSONAL_ACCESS_TOKEN"), remember_me=True)  # type: ignore
# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


def custom_error_handler(err):
    my_logger = Logger("Custom Dash Error Handler")
    body = f"""
        Error {str(err)}
        Trackback info: {traceback.format_exc()}\n\n
    """
    my_logger.error(body)
    set_props(
        "error-output-div", dict(style={"display": "grid", "justifyContent": "center"})
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
        html.Div(
            id="error-output-div",
            style={"display": "none", "color": "red", "fontSize": "30px"},
            children="An error has occurred. Contact lancaster.joshua.c@gmail.com.",
        ),
        page_container,
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
    app.run(debug=True)
