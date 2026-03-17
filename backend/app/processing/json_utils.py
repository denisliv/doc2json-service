"""Утилиты для работы с извлечённым JSON: нормализация порядка ключей по схеме."""

from app.document_types.extraction_models import (
    AccountingStatementsModel,
    OfficialRequestModel,
)
from app.document_types.extraction_models.accounting_statements import TablesData

# Модели для нормализации (соответствие extraction_models, порядок как в 730-742)
EXTRACTION_MODELS = {
    "accounting_statements": AccountingStatementsModel,
    "official_request": OfficialRequestModel,
}

# Порядок для accounting после enrich_json: tables_data, message, xlsx
ACCOUNTING_ROOT_ORDER = ["tables_data", "message", "xlsx"]


def normalize_json_keys(data: dict, slug: str) -> dict:
    """Нормализует порядок ключей. Для accounting учитывает message/xlsx от enrich_json."""
    if slug == "accounting_statements":
        return _normalize_accounting(data)
    model_cls = EXTRACTION_MODELS.get(slug)
    if not model_cls:
        return data
    try:
        model = model_cls.model_validate(data)
        return model.model_dump(mode="json", by_alias=True)
    except Exception:
        return data


def _normalize_accounting(data: dict) -> dict:
    """Порядок: tables_data (с ключами из TablesData), message, xlsx."""
    result = {}
    tables_data = data.get("tables_data")
    if tables_data is not None:
        try:
            td = TablesData.model_validate(tables_data)
            result["tables_data"] = td.model_dump(mode="json", by_alias=True)
        except Exception:
            order = [
                "balance_head_table",
                "balance_dates_table",
                "balance_main_table_dates",
                "balance_main_table",
                "report_main_table",
            ]
            ordered = {k: tables_data[k] for k in order if k in tables_data}
            for k, v in tables_data.items():
                if k not in ordered:
                    ordered[k] = v
            result["tables_data"] = ordered
    for key in ["message", "xlsx"]:
        if key in data:
            result[key] = data[key]
    for key, value in data.items():
        if key not in result:
            result[key] = value
    return result if result else data
