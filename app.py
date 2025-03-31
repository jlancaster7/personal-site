from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
    callback,
    set_props,
    State,
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

# Simple CSS for the sidebar
sidebar_style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "height": "100%",
    "width": "250px",  # The default width of the sidebar
    # "padding": "20px",
    "backgroundColor": "#f8f9fa",
    "transition": "margin-left 0.3s",
    # We'll initially slide it completely to the left by default,
    # making it invisible on page load:
    "marginLeft": "-250px",
}
page_header_style = {
    "display": "grid",
    "gridAutoFlow": "column",
    "gridTemplateColumns": "100%",
    "backgroundColor": "#023020",
    "color": "white",
    "marginLeft": "0px",
    "transition": "margin-left 0.3s",
}

content_style = {
    "marginLeft": "0px",
    "transition": "margin-left 0.3s",
    "padding": "20px",
}

app.layout = html.Div(
    style={"backgroundColor": "#f9f9f9"},
    children=[
        html.Div(id="page-load-callback-initializer", style={"display": "none"}),
        html.Div(
            id="sidebar",
            style=sidebar_style,
            children=[
                html.Div(
                    style={
                        "padding": "20px",
                    },
                    children=[
                        html.H2("Sidebar Menu"),
                        html.Hr(),
                        html.Div(
                            [
                                dcc.Link("Home", href="/", style={"display": "block"}),
                                dcc.Link(
                                    "PCA", href="/pca", style={"display": "block"}
                                ),
                                dcc.Link(
                                    "Factor Analysis",
                                    href="/f-f-portfolio",
                                    style={"display": "block"},
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="page-header",
            style=page_header_style,
            children=[
                html.Button(
                    "☰",
                    id="sidebar-toggle",
                    n_clicks=0,
                    style={
                        "fontSize": "1.2rem",
                        "cursor": "pointer",
                        "border": "none",
                        "color": "white",
                        "zIndex": "1000",
                        "background": "transparent",
                        "marginBottom": "10px",
                        "padding": "10px",  # Increase clickable area
                        "width": "40px",  # Set desired width
                        "height": "40px",  # Set desired height
                    },
                ),
            ],
        ),
        html.Div(
            id="content",
            style=content_style,
            children=[
                page_container,
            ],
        ),
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


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-header", "style"),
        Output("content", "style"),
    ],
    [Input("sidebar-toggle", "n_clicks")],
    [
        State("sidebar", "style"),
        State("page-header", "style"),
        State("content", "style"),
    ],
)
def toggle_sidebar(
    n_clicks, sidebar_style_state, page_header_style_state, content_style_state
):
    """
    Toggle the sidebar in or out by adjusting the margin-left of both the sidebar and the content.
    """
    if n_clicks % 2 == 1:
        # Slide the sidebar into view
        sidebar_style_state["marginLeft"] = "0px"
        # Push the content to the right
        content_style_state["marginLeft"] = "250px"
        page_header_style_state["marginLeft"] = "250px"
    else:
        # Slide the sidebar out of view
        sidebar_style_state["marginLeft"] = "-250px"
        # Reset the content margin
        content_style_state["marginLeft"] = "0px"
        page_header_style_state["marginLeft"] = "0px"

    return sidebar_style_state, page_header_style_state, content_style_state


# @callback(
#     Output("page-header", "children"),
#     Input("page-load-callback-initializer", "children"),
# )
# def initialize_header(_):
#     return [
#         html.Div(
#             style={"display": "grid", "gridAutoFlow": "column"},
#             children=[
#                 html.H1(
#                     style={
#                         "display": "grid",
#                         "width": "fit-content",
#                         "whitespace": "nowrap",
#                         "color": "white",
#                         "padding": "8px",
#                         "paddingRight": "24px",
#                     },
#                     children=dcc.Link(
#                         href=page["relative_path"], children=f"{page['name']}"
#                     ),
#                 )
#                 for page in page_registry.values()
#             ],
#         )
#     ]


if __name__ == "__main__":
    if is_heroku:
        app.run(debug=False)
    else:
        app.run(debug=True)
