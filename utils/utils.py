import io
import logging
from typing import Any
from dash import html
import time
import base64
import inspect
from datetime import datetime, timedelta
import pandas as pd


def parse_file_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div(["Unsupported file format"])
    except Exception as e:
        return html.Div(["Error processing file."])


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def time_function(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time} seconds")
        return result

    return wrapper


class Logger:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s -%(message)s"
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)


class BaseClass(Logger):
    def __init__(self, name: str, environment: str) -> None:
        super().__init__(name)
        self.environment = environment
        if self.environment == "dev":
            self._wrap_methods_with_timer()

    def _wrap_methods_with_timer(self):
        for attr_name in dir(self):
            if callable(getattr(self, attr_name)) and not attr_name.startswith("_"):
                method = getattr(self, attr_name)
                if inspect.iscoroutinefunction(method):
                    continue
                decorated_method = time_function(method)
                setattr(self, attr_name, decorated_method)
