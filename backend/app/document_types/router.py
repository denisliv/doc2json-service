import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import jsonschema

from app.auth.dependencies import get_current_user, require_role
from app.auth.models import User
from app.common.exceptions import BadRequestError, ConflictError, NotFoundError
from app.database import get_db
from app.document_types.schemas import (
    DocumentTypeCreate,
    DocumentTypeListItem,
    DocumentTypeResponse,
    DocumentTypeUpdate,
    DocumentTypeVersionResponse,
    PluginInfo,
    TestPromptRequest,
    TestPromptResponse,
)
from app.document_types.service import (
    create_document_type,
    deactivate_document_type,
    get_document_type,
    get_versions,
    list_document_types,
    update_document_type,
)
from app.processing.postprocessing import list_available_plugins

router = APIRouter()


@router.get("", response_model=list[DocumentTypeListItem])
async def list_types(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    types = await list_document_types(db)
    return types


@router.get("/plugins", response_model=list[PluginInfo])
async def get_plugins(user: User = Depends(require_role("admin"))):
    return list_available_plugins()


@router.get("/{slug}", response_model=DocumentTypeResponse)
async def get_type(
    slug: str,
    user: User = Depends(require_role("manager")),
    db: AsyncSession = Depends(get_db),
):
    dt = await get_document_type(db, slug)
    if not dt:
        raise NotFoundError("Document type not found")
    return dt


@router.post(
    "",
    response_model=DocumentTypeResponse,
    status_code=201,
    summary="Create document type",
    description="Create a new document type. Provide a full JSON Schema in `json_schema`: define `type`, `properties`, and `description` for each key (and nested keys) so the LLM and validation use the same structure.",
)
async def create_type(
    body: DocumentTypeCreate,
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    existing = await get_document_type(db, body.slug)
    if existing:
        raise ConflictError(f"Document type '{body.slug}' already exists")
    return await create_document_type(db, body, user.id)


@router.put(
    "/{slug}",
    response_model=DocumentTypeResponse,
    summary="Update document type",
    description="Update a document type. You can set a full JSON Schema with structure and descriptions for each key.",
)
async def update_type(
    slug: str,
    body: DocumentTypeUpdate,
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    dt = await update_document_type(db, slug, body, user.id)
    if not dt:
        raise NotFoundError("Document type not found")
    return dt


@router.delete("/{slug}")
async def delete_type(
    slug: str,
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    success = await deactivate_document_type(db, slug)
    if not success:
        raise NotFoundError("Document type not found")
    return {"detail": "Document type deactivated"}


@router.get("/{slug}/versions", response_model=list[DocumentTypeVersionResponse])
async def get_type_versions(
    slug: str,
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    return await get_versions(db, slug)


@router.post("/{slug}/test", response_model=TestPromptResponse)
async def test_type(
    slug: str,
    body: TestPromptRequest,
    user: User = Depends(require_role("manager")),
    db: AsyncSession = Depends(get_db),
):
    dt = await get_document_type(db, slug)
    if not dt:
        raise NotFoundError("Document type not found")

    start = time.time()
    try:
        from app.processing.json_utils import normalize_json_keys
        from app.processing.llm_service import LLMService
        from app.processing.postprocessing import apply_postprocessors

        doc_type_dict = {
            "slug": dt.slug,
            "name": dt.name,
            "json_schema": dt.json_schema,
            "system_prompt": dt.system_prompt,
            "user_prompt": dt.user_prompt,
            "markdown_postprocessors": dt.markdown_postprocessors or [],
            "json_postprocessors": dt.json_postprocessors or [],
        }

        markdown = body.sample_text
        context = {"document_type_slug": dt.slug, "job_id": "test"}
        if doc_type_dict["markdown_postprocessors"]:
            markdown = apply_postprocessors(doc_type_dict["markdown_postprocessors"], markdown, context)

        llm = LLMService()
        extracted = llm.extract(markdown, doc_type_dict)
        extracted = normalize_json_keys(extracted, doc_type_dict["slug"])

        if doc_type_dict["json_postprocessors"]:
            extracted = apply_postprocessors(doc_type_dict["json_postprocessors"], extracted, context)

        errors = []
        validator = jsonschema.Draft202012Validator(dt.json_schema)
        for err in validator.iter_errors(extracted):
            errors.append({
                "path": ".".join(str(p) for p in err.absolute_path) or "$",
                "message": err.message,
            })

        elapsed = int((time.time() - start) * 1000)
        return TestPromptResponse(
            detected_type=dt.slug,
            extracted_json=extracted,
            is_valid=len(errors) == 0,
            validation_errors=errors if errors else None,
            processing_time_ms=elapsed,
        )
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        raise BadRequestError(f"Test failed: {e}")
