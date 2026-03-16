"""Document types CRUD with versioning."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.document_types.models import DocumentType, DocumentTypeVersion
from app.document_types.schemas import DocumentTypeCreate, DocumentTypeUpdate


async def list_document_types(db: AsyncSession, include_inactive: bool = False) -> list[DocumentType]:
    query = select(DocumentType).order_by(DocumentType.name)
    if not include_inactive:
        query = query.where(DocumentType.is_active.is_(True))
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_document_type(db: AsyncSession, slug: str) -> DocumentType | None:
    result = await db.execute(select(DocumentType).where(DocumentType.slug == slug))
    return result.scalar_one_or_none()


async def create_document_type(db: AsyncSession, data: DocumentTypeCreate, user_id: UUID | None = None) -> DocumentType:
    dt = DocumentType(
        slug=data.slug,
        name=data.name,
        description=data.description,
        json_schema=data.json_schema,
        system_prompt=data.system_prompt,
        user_prompt=data.user_prompt,
        router_hints=data.router_hints,
        markdown_postprocessors=data.markdown_postprocessors,
        json_postprocessors=data.json_postprocessors,
        created_by=user_id,
    )
    db.add(dt)
    await db.commit()
    await db.refresh(dt)
    return dt


async def update_document_type(
    db: AsyncSession, slug: str, data: DocumentTypeUpdate, user_id: UUID | None = None
) -> DocumentType | None:
    dt = await get_document_type(db, slug)
    if not dt:
        return None

    version_snapshot = DocumentTypeVersion(
        document_type_id=dt.id,
        version=dt.version,
        json_schema=dt.json_schema,
        system_prompt=dt.system_prompt,
        user_prompt=dt.user_prompt,
        router_hints=dt.router_hints,
        markdown_postprocessors=dt.markdown_postprocessors or [],
        json_postprocessors=dt.json_postprocessors or [],
        changed_by=user_id,
    )
    db.add(version_snapshot)

    update_fields = data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(dt, field, value)
    dt.version += 1

    await db.commit()
    await db.refresh(dt)
    return dt


async def deactivate_document_type(db: AsyncSession, slug: str) -> bool:
    dt = await get_document_type(db, slug)
    if not dt:
        return False
    dt.is_active = False
    await db.commit()
    return True


async def get_versions(db: AsyncSession, slug: str) -> list[DocumentTypeVersion]:
    dt = await get_document_type(db, slug)
    if not dt:
        return []
    result = await db.execute(
        select(DocumentTypeVersion)
        .where(DocumentTypeVersion.document_type_id == dt.id)
        .order_by(DocumentTypeVersion.version.desc())
    )
    return list(result.scalars().all())
