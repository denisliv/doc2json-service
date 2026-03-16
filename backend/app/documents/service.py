"""Document upload and job management service."""

import uuid
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.common.storage import delete_job_files, get_upload_dir, save_file
from app.document_types.models import DocumentType
from app.documents.models import Job, JobFile
from app.processing.tasks import process_job


async def create_job(
    db: AsyncSession,
    files: list[UploadFile],
    document_type_slug: str | None = None,
    user_id: UUID | None = None,
) -> Job:
    doc_type_id = None
    if document_type_slug:
        result = await db.execute(
            select(DocumentType).where(DocumentType.slug == document_type_slug, DocumentType.is_active.is_(True))
        )
        dt = result.scalar_one_or_none()
        if dt:
            doc_type_id = dt.id

    job_id = uuid.uuid4()
    job = Job(id=job_id, document_type_id=doc_type_id, created_by=user_id)
    db.add(job)

    upload_dir = get_upload_dir(str(job_id))
    for i, file in enumerate(files):
        content = await file.read()
        filepath = save_file(upload_dir, file.filename, content)
        job_file = JobFile(
            job_id=job_id,
            original_name=file.filename,
            storage_path=str(filepath),
            file_size=len(content),
            sort_order=i,
        )
        db.add(job_file)

    await db.commit()
    await db.refresh(job, attribute_names=["files"])

    process_job.delay(str(job_id))
    return job


async def get_job(db: AsyncSession, job_id: UUID) -> Job | None:
    result = await db.execute(
        select(Job).options(selectinload(Job.files)).where(Job.id == job_id)
    )
    return result.scalar_one_or_none()


async def list_jobs(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    user_id: UUID | None = None,
    all_jobs: bool = False,
) -> tuple[list[Job], int]:
    query = select(Job).options(selectinload(Job.files))
    count_query = select(func.count(Job.id))

    if status:
        query = query.where(Job.status == status)
        count_query = count_query.where(Job.status == status)

    if user_id and not all_jobs:
        query = query.where(Job.created_by == user_id)
        count_query = count_query.where(Job.created_by == user_id)

    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(Job.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def retry_job(db: AsyncSession, job_id: UUID) -> Job | None:
    job = await get_job(db, job_id)
    if not job:
        return None
    job.status = "pending"
    job.error_message = None
    job.extracted_json = None
    job.validation_errors = None
    job.is_valid = None
    job.markdown_result = None
    job.processing_time_ms = None
    job.started_at = None
    job.completed_at = None
    job.retry_count += 1
    await db.commit()
    process_job.delay(str(job_id))
    return job


async def delete_job(db: AsyncSession, job_id: UUID) -> bool:
    job = await get_job(db, job_id)
    if not job:
        return False
    delete_job_files(str(job_id))
    await db.delete(job)
    await db.commit()
    return True
