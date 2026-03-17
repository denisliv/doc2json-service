"""External API: synchronous OCR and full pipeline endpoints (no auth required)."""

import tempfile
import time
from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile
from sqlalchemy import select

from app.database import async_session_factory
from app.document_types.models import DocumentType
from app.document_types.service import document_type_to_dict
from app.processing.json_utils import normalize_json_keys
from app.processing.llm_service import LLMService
from app.processing.ocr_service import OCRService
from app.processing.postprocessing import apply_postprocessors
from app.validation.service import validate_json

router = APIRouter()


@router.post("/extract-text")
async def extract_text(files: list[UploadFile] = File(...)):
    """PDF(s) -> Markdown (OCR only, no LLM)."""
    start = time.time()
    temp_paths = []
    try:
        for f in files:
            content = await f.read()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(content)
            tmp.close()
            temp_paths.append(tmp.name)

        ocr = OCRService()
        markdown = ocr.process_files(temp_paths)
        elapsed = int((time.time() - start) * 1000)
        return {"markdown": markdown, "processing_time_ms": elapsed}
    finally:
        for p in temp_paths:
            Path(p).unlink(missing_ok=True)


@router.post("/extract-json")
async def extract_json(
    files: list[UploadFile] = File(...),
    document_type_slug: str | None = Form(None),
):
    """PDF(s) -> JSON (full pipeline, synchronous)."""
    start = time.time()
    temp_paths = []
    try:
        for f in files:
            content = await f.read()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(content)
            tmp.close()
            temp_paths.append(tmp.name)

        # 1. OCR
        ocr = OCRService()
        markdown = ocr.process_files(temp_paths)

        # 2. Determine document type
        async with async_session_factory() as session:
            doc_type_dict = None
            detected_slug = None

            if document_type_slug:
                result = await session.execute(
                    select(DocumentType).where(
                        DocumentType.slug == document_type_slug,
                        DocumentType.is_active.is_(True),
                    )
                )
                dt = result.scalar_one_or_none()
                if dt:
                    doc_type_dict = document_type_to_dict(dt)
                    detected_slug = dt.slug

            if doc_type_dict is None:
                active_result = await session.execute(
                    select(DocumentType).where(DocumentType.is_active.is_(True))
                )
                active_types = [document_type_to_dict(dt) for dt in active_result.scalars().all()]
                llm = LLMService()
                detected_slug = llm.route(markdown, active_types)

                if detected_slug != "other":
                    dt_result = await session.execute(
                        select(DocumentType).where(DocumentType.slug == detected_slug)
                    )
                    dt = dt_result.scalar_one_or_none()
                    if dt:
                        doc_type_dict = document_type_to_dict(dt)

        if doc_type_dict is None:
            elapsed = int((time.time() - start) * 1000)
            return {
                "detected_type": detected_slug or "other",
                "is_valid": False,
                "extracted_json": {"error": "Document type not recognized"},
                "validation_errors": None,
                "processing_time_ms": elapsed,
            }

        context = {"document_type_slug": detected_slug, "job_id": "sync"}

        # 3. Markdown postprocessing
        if doc_type_dict.get("markdown_postprocessors"):
            markdown = apply_postprocessors(doc_type_dict["markdown_postprocessors"], markdown, context)

        # 4. Extraction
        llm = LLMService()
        extracted = llm.extract(markdown, doc_type_dict)
        extracted = normalize_json_keys(extracted, doc_type_dict["slug"])

        # 5. JSON postprocessing
        if doc_type_dict.get("json_postprocessors"):
            extracted = apply_postprocessors(doc_type_dict["json_postprocessors"], extracted, context)

        # 6. Validation
        errors = validate_json(extracted, doc_type_dict["json_schema"])

        elapsed = int((time.time() - start) * 1000)
        return {
            "detected_type": detected_slug,
            "is_valid": len(errors) == 0,
            "extracted_json": extracted,
            "validation_errors": errors if errors else None,
            "processing_time_ms": elapsed,
        }
    finally:
        for p in temp_paths:
            Path(p).unlink(missing_ok=True)
