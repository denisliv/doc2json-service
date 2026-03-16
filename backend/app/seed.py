"""Seed built-in document types on first startup."""

import logging

from sqlalchemy import select

from app.database import async_session_factory
from app.document_types.models import DocumentType
from app.document_types.seed_types import BUILTIN_TYPES

logger = logging.getLogger(__name__)


async def seed_initial_data() -> None:
    async with async_session_factory() as session:
        await _seed_document_types(session)
        await session.commit()


async def _seed_document_types(session) -> None:
    for dt_data in BUILTIN_TYPES:
        result = await session.execute(
            select(DocumentType).where(DocumentType.slug == dt_data["slug"])
        )
        if result.scalar_one_or_none():
            continue
        dt = DocumentType(**dt_data)
        session.add(dt)
        logger.info("Seeded document type: %s", dt_data["slug"])
