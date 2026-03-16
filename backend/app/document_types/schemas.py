from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentTypeCreate(BaseModel):
    slug: str
    name: str
    description: str | None = None
    json_schema: dict
    system_prompt: str
    user_prompt: str
    router_hints: str | None = None
    markdown_postprocessors: list[str] = []
    json_postprocessors: list[str] = []


class DocumentTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    json_schema: dict | None = None
    system_prompt: str | None = None
    user_prompt: str | None = None
    router_hints: str | None = None
    markdown_postprocessors: list[str] | None = None
    json_postprocessors: list[str] | None = None


class DocumentTypeResponse(BaseModel):
    id: UUID
    slug: str
    name: str
    description: str | None
    json_schema: dict
    system_prompt: str
    user_prompt: str
    router_hints: str | None
    markdown_postprocessors: list[str]
    json_postprocessors: list[str]
    is_active: bool
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentTypeListItem(BaseModel):
    id: UUID
    slug: str
    name: str
    description: str | None
    is_active: bool
    version: int

    model_config = {"from_attributes": True}


class DocumentTypeVersionResponse(BaseModel):
    id: UUID
    version: int
    json_schema: dict
    system_prompt: str
    user_prompt: str
    router_hints: str | None
    markdown_postprocessors: list[str]
    json_postprocessors: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class TestPromptRequest(BaseModel):
    sample_text: str


class TestPromptResponse(BaseModel):
    detected_type: str | None
    extracted_json: dict | None
    is_valid: bool | None
    validation_errors: list[dict] | None
    processing_time_ms: int


class PluginInfo(BaseModel):
    name: str
    type: str
    description: str
