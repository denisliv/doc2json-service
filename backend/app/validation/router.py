from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import NotFoundError
from app.database import get_db
from app.document_types.service import get_document_type
from app.documents.service import get_job
from app.validation.service import validate_json

router = APIRouter()


class ValidateRequest(BaseModel):
    document_type_slug: str
    data: dict


class ValidateResponse(BaseModel):
    is_valid: bool
    errors: list[dict]
    errors_count: int
    warnings_count: int = 0


@router.post("", response_model=ValidateResponse)
async def validate_data(
    body: ValidateRequest,
    db: AsyncSession = Depends(get_db),
):
    dt = await get_document_type(db, body.document_type_slug)
    if not dt:
        raise NotFoundError("Document type not found")

    errors = validate_json(body.data, dt.json_schema)
    return ValidateResponse(
        is_valid=len(errors) == 0,
        errors=errors,
        errors_count=len(errors),
    )


@router.post("/job/{job_id}", response_model=ValidateResponse)
async def revalidate_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    job = await get_job(db, job_id)
    if not job or not job.extracted_json or not job.detected_type_slug:
        raise NotFoundError("Job not found or has no result")

    dt = await get_document_type(db, job.detected_type_slug)
    if not dt:
        raise NotFoundError("Document type not found")

    errors = validate_json(job.extracted_json, dt.json_schema)

    job.validation_errors = errors if errors else None
    job.is_valid = len(errors) == 0
    await db.commit()

    return ValidateResponse(
        is_valid=len(errors) == 0,
        errors=errors,
        errors_count=len(errors),
    )


@router.get("/schema/{slug}")
async def get_schema(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    dt = await get_document_type(db, slug)
    if not dt:
        raise NotFoundError("Document type not found")
    return dt.json_schema
