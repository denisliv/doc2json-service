"""
Pydantic models for built-in document types (aligned with Doc2JSON).
JSON Schema is generated from these models for LLM format_instructions and validation.
"""

from app.document_types.extraction_models.accounting_statements import (
    AccountingStatementsModel,
)
from app.document_types.extraction_models.official_request import OfficialRequestModel


def get_accounting_statements_json_schema() -> dict:
    """Return full JSON Schema for accounting statements (all keys and descriptions)."""
    return AccountingStatementsModel.model_json_schema(mode="serialization")


def get_official_request_json_schema() -> dict:
    """Return full JSON Schema for official request (all keys and descriptions)."""
    return OfficialRequestModel.model_json_schema(mode="serialization")
