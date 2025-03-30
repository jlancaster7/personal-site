import time
from datetime import datetime, timedelta
import snowflake.connector
from snowflake.connector.errors import ProgrammingError, OperationalError
import os
import requests
from pandas import DataFrame
from typing import Any
from utils.utils import BaseClass


class SnowflakeConnector(BaseClass):
    _instance = None

    def __new__(cls, environment, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SnowflakeConnector, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, environment):
        if not hasattr(self, "engine_initialized"):
            super().__init__("SnowflakeConnector", environment)
            self.engine = self.get_engine()
            self.engine_initialized = True

    def get_engine(self) -> snowflake.connector.SnowflakeConnection:
        if "SNOWFLAKE_USER" not in os.environ:
            raise Exception("Cannot connect to Snowflake. env vars are not set up.")
        account = os.getenv(f"SNOWFLAKE_ACCOUNT_IDENTIFIER")
        user = os.getenv(f"SNOWFLAKE_USER")
        password = os.getenv(f"SNOWFLAKE_PASSWORD")
        conn: snowflake.connector.SnowflakeConnection = snowflake.connector.connect(
            user=user, account=account, password=password
        )
        self.logger.info(f"Connected to snowflake db as {user}. Account={account}")
        return conn
    def get_user_portfolios(self, user_id: int) -> DataFrame:
        query = self._load_sql("sql/user_portfolios.sql")
        query = query.format(
            user_id=user_id
        )
        result = self._query(query)
        return result
    def get_most_recent_prices(self, ticker_list: list[str]) -> DataFrame:
        ticker_list_str = '(' + ', '.join(["'" + ticker + "'" for ticker in ticker_list]) + ')'

        query = self._load_sql("sql/most_recent_stock_prices.sql")
        query = query.format(
            ticker_list=ticker_list_str
        )
        result = self._query(query)
        return result

    def query_test(self):
        query = self._load_sql("sql/market_data_test.sql")

        result = self._query(query)
        return result

    def _load_sql(self, file_path: str):
        with open(file_path, "r") as file:
            return file.read()

    def _query(
        self, sql: str, max_retries: int = 3, retry_delay: float = 2.0
    ) -> DataFrame:
        for attempt in range(1, max_retries + 1):
            try:
                with self.engine.cursor() as cursor:
                    cursor.execute(sql)
                    data: DataFrame = cursor.fetch_pandas_all()
                    data.columns = data.columns.str.lower()
                    return data
            except (ProgrammingError, OperationalError) as e:
                self.logger.error(f"Queery failed on attempt {attempt}. Error {e}")
                if attempt < max_retries:
                    self.logger.info(f"Retrying in {retry_delay} seconds..")
                    time.sleep(retry_delay)
                else:
                    self.logger.error("Max retries reached. Raising exception.")
                    raise
            except Exception as e:
                self.logger.error(f"Queery failed on attempt {attempt}. Error {e}")
                if attempt < max_retries:
                    self.logger.info(f"Retrying in {retry_delay} seconds..")
                    time.sleep(retry_delay)
                else:
                    self.logger.error("Max retries reached. Raising exception.")
                    raise
        raise RuntimeError(
            "Unreachable _query ended without returning or raising ealier"
        )

    def _execute(self, sql, params) -> None:
        with self.engine.cursor() as cursor:
            cursor.execute(sql, params)
