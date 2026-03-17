"""Processing pipeline: OCR -> Postprocess MD -> Router -> Extract -> Postprocess JSON -> Validate -> Save."""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import jsonschema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from app.config import settings
import app.auth.models  # noqa: F401 — register User table for FK resolution
from app.document_types.models import DocumentType
from app.documents.models import Job, JobFile
from app.processing.json_utils import normalize_json_keys
from app.processing.llm_service import LLMService
from app.processing.ocr_service import OCRService
from app.processing.postprocessing import apply_postprocessors

logger = logging.getLogger(__name__)


def run_pipeline(job_id: str) -> None:
    """Synchronous pipeline entry point for Celery worker."""
    import asyncio
    asyncio.run(_run_pipeline_async(job_id))


async def _run_pipeline_async(job_id: str) -> None:
    start_time = time.time()

    engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        await _execute_pipeline(session_factory, job_id, start_time)
    finally:
        await engine.dispose()


async def _execute_pipeline(
    session_factory: async_sessionmaker[AsyncSession], job_id: str, start_time: float
) -> None:
    async with session_factory() as session:
        result = await session.execute(
            select(Job).options(selectinload(Job.files)).where(Job.id == job_id)
        )
        job = result.scalar_one_or_none()
        if not job:
            logger.error("Job %s not found", job_id)
            return

        try:
            job.status = "ocr_in_progress"
            job.started_at = datetime.now(timezone.utc)
            await session.commit()

            # 1. OCR
            pdf_paths = [f.storage_path for f in sorted(job.files, key=lambda f: f.sort_order)]
            ocr_service = OCRService()
            markdown = ocr_service.process_files(pdf_paths)

            # 2. Determine document type
            doc_type_dict = None
            if job.document_type_id:
                dt_result = await session.execute(
                    select(DocumentType).where(DocumentType.id == job.document_type_id)
                )
                dt = dt_result.scalar_one_or_none()
                if dt:
                    doc_type_dict = _dt_to_dict(dt)
                    job.detected_type_slug = dt.slug

            if doc_type_dict is None:
                # Route dynamically
                job.status = "routing"
                await session.commit()

                active_result = await session.execute(
                    select(DocumentType).where(DocumentType.is_active.is_(True))
                )
                active_types = [_dt_to_dict(dt) for dt in active_result.scalars().all()]

                llm = LLMService()
                detected_slug = llm.route(markdown, active_types)
                job.detected_type_slug = detected_slug

                if detected_slug != "other":
                    dt_result = await session.execute(
                        select(DocumentType).where(DocumentType.slug == detected_slug)
                    )
                    dt = dt_result.scalar_one_or_none()
                    if dt:
                        doc_type_dict = _dt_to_dict(dt)

            if doc_type_dict is None:
                job.status = "completed"
                job.extracted_json = {"error": "Document type not recognized"}
                job.is_valid = False
                job.completed_at = datetime.now(timezone.utc)
                job.processing_time_ms = int((time.time() - start_time) * 1000)
                await session.commit()
                return

            # 3. Markdown postprocessing
            context = {"document_type_slug": doc_type_dict["slug"], "job_id": job_id}
            if doc_type_dict.get("markdown_postprocessors"):
                markdown = apply_postprocessors(doc_type_dict["markdown_postprocessors"], markdown, context)

            job.markdown_result = markdown
            _save_markdown(job_id, markdown)

            # 4. Extraction
            job.status = "extracting"
            await session.commit()

            llm = LLMService()
            extracted = llm.extract(markdown, doc_type_dict)

            # 4b. Нормализация порядка ключей по схеме (accounting_statements.py и др.)
            extracted = normalize_json_keys(extracted, doc_type_dict["slug"])

            # 5. JSON postprocessing
            if doc_type_dict.get("json_postprocessors"):
                extracted = apply_postprocessors(doc_type_dict["json_postprocessors"], extracted, context)

            # 6. Validation
            job.status = "validating"
            await session.commit()

            validation_errors = _validate_json(extracted, doc_type_dict["json_schema"])
            job.extracted_json = extracted
            job.is_valid = len(validation_errors) == 0
            job.validation_errors = validation_errors if validation_errors else None

            _save_result(job_id, extracted)

            job.status = "completed"
            job.completed_at = datetime.now(timezone.utc)
            job.processing_time_ms = int((time.time() - start_time) * 1000)
            await session.commit()

            logger.info("Job %s completed in %d ms", job_id, job.processing_time_ms)

        except Exception as e:
            logger.exception("Job %s failed: %s", job_id, e)
            job.status = "failed"
            job.error_message = str(e)[:2000]
            job.completed_at = datetime.now(timezone.utc)
            job.processing_time_ms = int((time.time() - start_time) * 1000)
            await session.commit()


def _dt_to_dict(dt: DocumentType) -> dict:
    return {
        "slug": dt.slug,
        "name": dt.name,
        "description": dt.description,
        "json_schema": dt.json_schema,
        "system_prompt": dt.system_prompt,
        "user_prompt": dt.user_prompt,
        "router_hints": dt.router_hints,
        "markdown_postprocessors": dt.markdown_postprocessors or [],
        "json_postprocessors": dt.json_postprocessors or [],
    }


def _validate_json(data: dict, schema: dict) -> list[dict]:
    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for error in validator.iter_errors(data):
        errors.append({
            "path": ".".join(str(p) for p in error.absolute_path) or "$",
            "message": error.message,
            "severity": "error",
        })
    return errors


def _save_markdown(job_id: str, markdown: str) -> None:
    from app.common.storage import get_markdown_dir
    md_dir = get_markdown_dir(job_id)
    (md_dir / "merged.md").write_text(markdown, encoding="utf-8")


def _save_result(job_id: str, data: dict) -> None:
    from app.common.storage import get_result_dir
    res_dir = get_result_dir(job_id)
    (res_dir / "result.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
