from dash import callback, Output, Input, State, no_update
from datetime import datetime
import numpy as np
from typing import cast
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from sklearn.decomposition import PCA
from openbb import obb
import dash_bootstrap_components as dbc

obb.user.preferences.output_type = "dataframe"  # type: ignore

pio.templates.default = "plotly"

page_prefix = "pca-"


def create_charts(
    bar_chart_data: np.ndarray,
    line_chart_data: np.ndarray,
    scatter_plot_data: pd.DataFrame,
    scatter_plot_labels,
    n_components,
):
    """
    Create the bar chart, line chart, and scatter plot based on the PCA analysis.
    """
    bar_chart = go.Figure(
        data=(
            [
                go.Bar(
                    x=["PC" + str(i + 1) for i in range(n_components)],
                    y=bar_chart_data,
                )
            ]
            if len(bar_chart_data)
            else []
        ),
        layout=go.Layout(
            title="Explained Variance by Components",
            xaxis=dict(title="Principal Components"),
            yaxis=dict(title="Explained Variance"),
        ),
    )
    line_chart = go.Figure(
        data=(
            [
                go.Scatter(
                    x=["PC" + str(i + 1) for i in range(n_components)],
                    y=line_chart_data,
                    mode="lines+markers",
                )
            ]
            if len(line_chart_data)
            else []
        ),
        layout=go.Layout(
            title="Cumulative Explained Variance",
            xaxis=dict(title="Principal Components"),
            yaxis=dict(title="Cumulative Explained Variance"),
        ),
    )
    scatter_plot = go.Figure(
        data=(
            [
                go.Scatter(
                    x=scatter_plot_data["f1"],
                    y=(
                        scatter_plot_data["f2"]
                        if n_components > 1
                        else np.zeros(len(scatter_plot_data))
                    ),
                    mode="markers+text",
                    text=scatter_plot_labels,
                    textposition="top center",
                )
            ]
            if not scatter_plot_data.empty
            else []
        ),
        layout=go.Layout(
            title="Scatter Plot of First Two Factors",
            xaxis=dict(title="Factor 1"),
            yaxis=(
                dict(title="Factor 2")
                # if n_components > 1
                # else dict(title="Factor 2 (Zero)")
            ),
        ),
    )

    return bar_chart, line_chart, scatter_plot


def register_callbacks():
    """
    Register callbacks for PCA analysis page.
    """

    @callback(
        Output(page_prefix + "bar-chart", "figure"),
        Output(page_prefix + "line-plot", "figure"),
        Output(page_prefix + "scatter-plot", "figure"),
        Input(page_prefix + "inputs-card", "children"),
    )
    def initialize_graphs(_):
        """
        Initialize the graphs with empty data.
        """
        bar_chart, line_chart, scatter_plot = create_charts(
            np.empty((0, 0)),
            np.empty((0)),
            pd.DataFrame(),
            [],
            0,
        )
        return bar_chart, line_chart, scatter_plot

    @callback(
        [
            Output(page_prefix + "bar-chart", "figure", allow_duplicate=True),
            Output(page_prefix + "line-plot", "figure", allow_duplicate=True),
            Output(page_prefix + "scatter-plot", "figure", allow_duplicate=True),
            Output("toast-message", "children", allow_duplicate=True),
            Output("toast-message", "is_open", allow_duplicate=True),
        ],
        [
            Input(page_prefix + "submit-button", "n_clicks"),
            Input(page_prefix + "ticker-input", "n_submit"),
        ],
        [
            State(page_prefix + "ticker-input", "value"),
            State(page_prefix + "components-dropdown", "value"),
            State(page_prefix + "date-picker", "start_date"),
            State(page_prefix + "date-picker", "end_date"),
        ],
        prevent_initial_call=True,
    )
    def update_graphs(
        n_clicks, ticker_input_submit, tickers, n_components, start_date, end_date
    ):
        if n_clicks is None and ticker_input_submit is None:
            return {}, {}, {}, no_update, no_update
        # Clean and validate ticker symbols
        if not tickers:
            return ({}, {}, {}, "Please enter at least one valid ticker symbol.", True)
        tickers = [
            ticker.strip().upper()  # Remove whitespace and convert to uppercase
            for ticker in tickers.split(",")
            if ticker.strip()  # Filter out empty strings
        ]

        if not tickers:
            return {}, {}, {}, "Please enter at least one valid ticker symbol.", True

        if len(tickers) < n_components:
            return {}, {}, {}, "Number of componets exceeds number of tickers.", True

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        data = obb.equity.price.historical(  # type: ignore
            tickers, start_date=start_date, end_date=end_date, provider="yfinance"
        )
        data = cast(pd.DataFrame, data)

        data = data.pivot(columns="symbol", values="close")
        daily_returns = data.pct_change().dropna()

        pca = PCA(n_components=n_components)
        pca.fit(daily_returns)
        explained_var_ratio = pca.explained_variance_ratio_

        cumulative_var_ratio = np.cumsum(explained_var_ratio)

        X = np.asarray(daily_returns)
        factor_returns = pd.DataFrame(
            columns=["f" + str(i + 1) for i in range(n_components)],
            index=daily_returns.index,
            data=X.dot(pca.components_.T),
        )
        factor_exposures = pd.DataFrame(
            index=["f" + str(i + 1) for i in range(n_components)],
            columns=daily_returns.columns,
            data=pca.components_,
        ).T
        labels = factor_exposures.index
        # data = factor_exposures.values

        bar_chart, line_chart, scatter_plot = create_charts(
            explained_var_ratio,
            cumulative_var_ratio,
            factor_exposures,
            labels,
            n_components,
        )
        return bar_chart, line_chart, scatter_plot, no_update, False
