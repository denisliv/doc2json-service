"""Добавляет поля message и xlsx к результату бухгалтерской отчётности.
Порядок ключей соответствует accounting_statements.py (730-742):
tables_data (с balance_head_table, balance_dates_table, balance_main_table_dates,
balance_main_table, report_main_table), message, xlsx."""

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
    # Порядок ключей как в TablesData (accounting_statements.py)
    ordered_tables = {k: tables_data[k] for k in REQUIRED_TABLES_KEYS if k in tables_data}
    for k in tables_data:
        if k not in ordered_tables:
            ordered_tables[k] = tables_data[k]
    message = {key: "OK" if key in tables_data else "Missing" for key in REQUIRED_TABLES_KEYS}
    # Порядок: tables_data, message, xlsx (как в схеме)
    return {"tables_data": ordered_tables, "message": message, "xlsx": None}
