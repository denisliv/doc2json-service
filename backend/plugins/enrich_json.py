"""Добавляет поля message и xlsx к результату бухгалтерской отчётности."""

PLUGIN_TYPE = "json"

REQUIRED_TABLES_KEYS = [
    "balance_head_table",
    "balance_dates_table",
    "balance_main_table_dates",
    "balance_main_table",
    "report_main_table",
]


def process(data, **context):
    if not isinstance(data, dict):
        return data
    tables_data = data.get("tables_data", {})
    message = {key: "OK" if key in tables_data else "Missing" for key in REQUIRED_TABLES_KEYS}
    return {"message": message, "xlsx": None, **data}
