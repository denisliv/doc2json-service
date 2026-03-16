from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UploadResponse(BaseModel):
    job_id: UUID
    status: str
    files_count: int
    status_url: str


class JobFileResponse(BaseModel):
    id: UUID
    name: str
    size: int | None

    model_config = {"from_attributes": True}


class JobResponse(BaseModel):
    id: UUID
    status: str
    detected_type: str | None = None
    is_valid: bool | None = None
    validation_errors: dict | list | None = None
    extracted_json: dict | None = None
    error_message: str | None = None
    files: list[JobFileResponse] = []
    processing_time_ms: int | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    page_size: int
