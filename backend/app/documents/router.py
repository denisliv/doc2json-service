from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, get_optional_user, require_role
from app.auth.models import User
from app.auth.service import has_role
from app.common.exceptions import NotFoundError
from app.database import get_db
from app.documents.schemas import JobListResponse, JobResponse, JobFileResponse, UploadResponse
from app.documents.service import create_job, delete_job, get_job, list_jobs, retry_job
from app.processing.json_utils import normalize_json_keys

router = APIRouter()


@router.post("/process", response_model=UploadResponse, status_code=202)
async def upload_and_process(
    files: list[UploadFile] = File(...),
    document_type_slug: str | None = Form(None),
    user: User | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = user.id if user else None
    job = await create_job(db, files, document_type_slug, user_id)
    return UploadResponse(
        job_id=job.id,
        status=job.status,
        files_count=len(job.files),
        status_url=f"/api/v1/documents/jobs/{job.id}",
    )


@router.get("/jobs", response_model=JobListResponse)
async def get_jobs(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    all_jobs = has_role(user.role, "manager")
    items, total = await list_jobs(db, page, page_size, status, user.id, all_jobs)
    return JobListResponse(
        items=[_job_to_response(j) for j in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_detail(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    job = await get_job(db, job_id)
    if not job:
        raise NotFoundError("Job not found")
    return _job_to_response(job)


@router.get("/jobs/{job_id}/result")
async def get_job_result(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    job = await get_job(db, job_id)
    if not job:
        raise NotFoundError("Job not found")
    extracted = job.extracted_json or {}
    if extracted and job.detected_type_slug:
        extracted = normalize_json_keys(extracted, job.detected_type_slug)
    return JSONResponse(content=extracted)


@router.get("/jobs/{job_id}/markdown")
async def get_job_markdown(
    job_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    job = await get_job(db, job_id)
    if not job:
        raise NotFoundError("Job not found")
    return {"markdown": job.markdown_result or ""}


@router.get("/jobs/{job_id}/files/{file_id}")
async def download_file(
    job_id: UUID,
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    job = await get_job(db, job_id)
    if not job:
        raise NotFoundError("Job not found")
    file = next((f for f in job.files if f.id == file_id), None)
    if not file:
        raise NotFoundError("File not found")
    path = Path(file.storage_path)
    if not path.exists():
        raise NotFoundError("File not found on disk")
    return FileResponse(path, filename=file.original_name, media_type="application/pdf")


@router.post("/jobs/{job_id}/retry", response_model=JobResponse)
async def retry_job_endpoint(
    job_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    job = await retry_job(db, job_id)
    if not job:
        raise NotFoundError("Job not found")
    return _job_to_response(job)


@router.delete("/jobs/{job_id}")
async def delete_job_endpoint(
    job_id: UUID,
    user: User = Depends(require_role("manager")),
    db: AsyncSession = Depends(get_db),
):
    deleted = await delete_job(db, job_id)
    if not deleted:
        raise NotFoundError("Job not found")
    return {"detail": "Job deleted"}


def _job_to_response(job) -> JobResponse:
    # JSONB в PostgreSQL не сохраняет порядок ключей — восстанавливаем при отдаче в API
    extracted = job.extracted_json
    if extracted and job.detected_type_slug:
        extracted = normalize_json_keys(extracted, job.detected_type_slug)
    return JobResponse(
        id=job.id,
        status=job.status,
        detected_type=job.detected_type_slug,
        is_valid=job.is_valid,
        validation_errors=job.validation_errors,
        extracted_json=extracted,
        error_message=job.error_message,
        files=[
            JobFileResponse(id=f.id, name=f.original_name, size=f.file_size)
            for f in (job.files or [])
        ],
        processing_time_ms=job.processing_time_ms,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
    )
