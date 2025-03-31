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
    callback_context,
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
        # 1) Track the current page, so we know when someone has navigated.
        dcc.Location(id="url", refresh=False),
        # 2) Keep track of whether the sidebar is open (True) or closed (False)
        dcc.Store(id="sidebar-open", data=False),
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
        Output("sidebar-open", "data"),  # updated open/closed state
    ],
    [
        Input("sidebar-toggle", "n_clicks"),
        Input("url", "pathname"),
    ],
    [  # triggers if the user navigates],
        State("sidebar", "style"),
        State("page-header", "style"),
        State("content", "style"),
        State("sidebar-open", "data"),  # the old open/closed state
    ],
)
def toggle_sidebar(
    n_clicks,
    pathname,
    sidebar_style_state,
    page_header_style_state,
    content_style_state,
    is_open,
):
    """
    1) If user navigates (i.e., url changes), automatically close the sidebar.
    2) Otherwise, if user clicks the toggle, flip the current open/closed state.
    """

    ctx = callback_context

    if not ctx.triggered:
        # no triggers => just return the same state
        return (
            sidebar_style_state,
            page_header_style_state,
            content_style_state,
            is_open,
        )

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Make copies of the style dictionaries so we don't mutate them in place
    new_sidebar_style = sidebar_style_state.copy()
    new_page_header_style = page_header_style_state.copy()
    new_content_style = content_style_state.copy()

    if triggered_id == "url":
        # user navigated => force close the sidebar
        new_sidebar_style["marginLeft"] = "-250px"
        new_content_style["marginLeft"] = "0px"
        new_page_header_style["marginLeft"] = "0px"
        return new_sidebar_style, new_page_header_style, new_content_style, False

    else:
        # user clicked the toggle button => flip open vs. closed
        new_is_open = not is_open
        if new_is_open:
            new_sidebar_style["marginLeft"] = "0px"
            new_content_style["marginLeft"] = "250px"
            new_page_header_style["marginLeft"] = "250px"
        else:
            new_sidebar_style["marginLeft"] = "-250px"
            new_content_style["marginLeft"] = "0px"
            new_page_header_style["marginLeft"] = "0px"

        return new_sidebar_style, new_page_header_style, new_content_style, new_is_open


if __name__ == "__main__":
    if is_heroku:
        app.run(debug=False)
    else:
        app.run(debug=True)
