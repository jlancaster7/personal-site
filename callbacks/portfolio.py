from dash import callback, Output, Input
from services.snow import SnowflakeConnector


def register_callbacks():
    @callback(
        Output("user-portfolio-table", "rowData"),
        Input("portfolio-page-load-callback-initializer", "children"),
    )
    def set_portfolio_table_data(_):
        db = SnowflakeConnector("dev")
        data = db.get_user_portfolios(1)
        data.sort_values(by="market_value", ascending=False, inplace=True)
        return data.to_dict("records")
