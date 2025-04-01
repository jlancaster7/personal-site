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
from pandas_datareader import data as pdr
from pandas_datareader.famafrench import get_available_datasets
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
from statsmodels.regression.rolling import RollingRegressionResults
from utils.utils import is_float


obb.user.preferences.output_type = "dataframe"  # type: ignore

pio.templates.default = "plotly"

page_prefix = "fama-french-"


def register_callbacks():
    @callback(
        [
            Output(page_prefix + "text-output-pre", "children"),
            Output(page_prefix + "rolling-coeffs-chart", "figure"),
            Output("toast-message", "children", allow_duplicate=True),
            Output("toast-message", "is_open", allow_duplicate=True),
        ],
        [
            Input(page_prefix + "submit-button", "n_clicks"),
            Input(page_prefix + "ticker-input", "n_submit"),
            Input(page_prefix + "weights-input", "n_submit"),
        ],
        [
            State(page_prefix + "ticker-input", "value"),
            State(page_prefix + "weights-input", "value"),
            State(page_prefix + "model-dropdown", "value"),
            State(page_prefix + "date-picker", "start_date"),
            State(page_prefix + "date-picker", "end_date"),
        ],
        prevent_initial_call=True,
    )
    def update_tables(
        n_clicks,
        ticker_input_submit,
        weights_input_submit,
        tickers,
        weights,
        model,
        start_date,
        end_date,
    ):
        if (
            n_clicks is None
            and ticker_input_submit is None
            and weights_input_submit is None
        ):
            return "", {}, no_update, no_update
        if tickers is None or weights is None:
            return "",{}, "Please enter valid ticker symbols and weights.", True
        tickers = [
            ticker.strip().upper()  # Remove whitespace and convert to uppercase
            for ticker in tickers.split(",")
            if ticker.strip()  # Filter out empty strings
        ]
        weights = [
            float(weight.strip())  # Convert to float after stripping whitespace
            for weight in weights.split(",")
            if weight.strip()
            and is_float(weight.strip())  # Check if it's a valid number
        ]

        if len(tickers) != len(weights):
            return (
                "",
                {},
                "The number of tickers and weights must match.",
                True,
            )
        if sum(weights) != 1:
            return (
                "",
                {},
                "The weights must sum to 1.",
                True,
            )
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        stock_prices = obb.equity.price.historical(  # type: ignore
            symbol=tickers, start_date=start_date, end_date=end_date
        )

        stock_prices = cast(pd.DataFrame, stock_prices)
        stock_prices = stock_prices.pivot(columns="symbol", values="close")
        stock_prices.index = pd.to_datetime(stock_prices.index)
        stock_returns = stock_prices.pct_change().dropna()

        portfolio_returns = (stock_returns * weights).sum(axis=1)
        portfolio_returns.name = "Portfolio"
        if 'SPY' in tickers:
            benchmark_returns = stock_returns.pop('SPY')
        else:
            benchmark_prices = obb.equity.price.historical(  # type: ignore
                symbol=tickers, start_date=start_date, end_date=end_date
            )   
            benchmark_prices = cast(pd.DataFrame, benchmark_prices)
            benchmark_prices = benchmark_prices.pivot(columns="symbol", values="close")
            benchmark_prices.index = pd.to_datetime(benchmark_prices.index)
            benchmark_returns = benchmark_prices.pct_change().dropna().pop('SPY')

        
        active_returns = (portfolio_returns - benchmark_returns).dropna()
        active_returns.name = "Active Returns"
        
        ff3_factors_daily = pdr.get_data_famafrench(
            "F-F_Research_Data_Factors_daily", start=start_date
        )[0]
        ff5_factors_daily = pdr.get_data_famafrench(
            "F-F_Research_Data_5_Factors_2x3_daily", start=start_date
        )[0]
            
        # Align factors with daily portfolio returns
        if model == "FF3":

            data = pd.merge(
                active_returns,
                ff3_factors_daily,
                left_index=True,
                right_index=True,
                how="inner",
            )
            factors = [
                # "Mkt-RF", 
                "SMB", "HML"]
        elif model == "FF5":
            data = pd.merge(
                active_returns,
                ff5_factors_daily,
                left_index=True,
                right_index=True,
                how="inner",
            )
            factors = [
                # "Mkt-RF", 
                "SMB", "HML", "RMW", "CMA"
                ]
        else:
            return "", {},"Invalid model selected.", True

        def factor_regression(
            data, factors
        ) -> sm.regression.linear_model.RegressionResultsWrapper:
            Y = (
                data["Active Returns"] * 100 # - data["RF"]
            )  # Convert returns to % for consistency
            X = data[factors]
            X = sm.add_constant(X)
            model = sm.OLS(Y, X).fit()
            return model
        def rolling_factor_regression(data: pd.DataFrame, factors: list[str]) -> RollingRegressionResults:
            exog = sm.add_constant(data[factors])    
            rols = RollingOLS(data['Active Returns'] * 100, exog, window=60)
            model = rols.fit()
            return model

        model_results = rolling_factor_regression(data, factors)
        ols_model_results = factor_regression(data, factors)
        model_summary = ols_model_results.summary().as_text()

        coeffs_df = model_results.params
        coeffs_df = coeffs_df.dropna()

        coeffs_df = cast(pd.DataFrame, coeffs_df)
        coeffs_df.index = pd.to_datetime(coeffs_df.index)
        
        fig = go.Figure()
        for col in coeffs_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=coeffs_df.index,
                    y=coeffs_df[col],
                    mode="lines",
                    name=col,
                )
            )

        return model_summary, fig, no_update, no_update
