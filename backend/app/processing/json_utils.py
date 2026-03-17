"""Утилиты для работы с извлечённым JSON: нормализация порядка ключей по схеме."""

from app.document_types.extraction_models import (
    AccountingStatementsModel,
    OfficialRequestModel,
)

# Модели для нормализации (соответствие extraction_models, порядок как в 730-742)
EXTRACTION_MODELS = {
    "accounting_statements": AccountingStatementsModel,
    "official_request": OfficialRequestModel,
}


def normalize_json_keys(data: dict, slug: str) -> dict:
    """Нормализует порядок ключей по Pydantic-модели."""
    model_cls = EXTRACTION_MODELS.get(slug)
    if not model_cls:
        return data
    try:
        model = model_cls.model_validate(data)
        return model.model_dump(mode="json", by_alias=True)
    except Exception:
        return data
