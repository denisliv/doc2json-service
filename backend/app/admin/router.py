from uuid import UUID

import redis
from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import UserCreate, UserUpdate
from app.auth.dependencies import require_role
from app.auth.models import User
from app.auth.schemas import UserResponse
from app.auth.service import hash_password
from app.common.exceptions import ConflictError, NotFoundError
from app.config import settings
from app.database import get_db

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).order_by(User.created_at))
    return list(result.scalars().all())


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(select(User).where(User.username == body.username))
    if existing.scalar_one_or_none():
        raise ConflictError(f"User '{body.username}' already exists")

    new_user = User(
        username=body.username,
        password_hash=hash_password(body.password),
        full_name=body.full_name,
        role=body.role,
        must_change_password=True,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    target = result.scalar_one_or_none()
    if not target:
        raise NotFoundError("User not found")

    if body.full_name is not None:
        target.full_name = body.full_name
    if body.role is not None:
        target.role = body.role
    if body.is_active is not None:
        target.is_active = body.is_active
    if body.password is not None:
        target.password_hash = hash_password(body.password)

    await db.commit()
    await db.refresh(target)
    return target


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: UUID,
    user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    if str(user.id) == str(user_id):
        raise ConflictError("Cannot deactivate yourself")

    result = await db.execute(select(User).where(User.id == user_id))
    target = result.scalar_one_or_none()
    if not target:
        raise NotFoundError("User not found")
    target.is_active = False
    await db.commit()
    return {"detail": "User deactivated"}


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    components = {}

    # Database
    try:
        await db.execute(text("SELECT 1"))
        components["database"] = {"status": "up"}
    except Exception as e:
        components["database"] = {"status": "down", "error": str(e)}

    # Redis
    try:
        r = redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        r.ping()
        components["redis"] = {"status": "up"}
        r.close()
    except Exception as e:
        components["redis"] = {"status": "down", "error": str(e)}

    # LLM
    try:
        import httpx
        resp = httpx.get(f"{settings.LLM_API_URL}/models", timeout=5)
        components["llm_vllm"] = {"status": "up", "model": settings.LLM_MODEL_NAME}
    except Exception:
        components["llm_vllm"] = {"status": "down"}

    # OCR
    try:
        import httpx
        resp = httpx.get(f"{settings.OCR_VL_SERVER_URL}/models", timeout=5)
        components["ocr_vllm"] = {"status": "up", "model": settings.OCR_VL_MODEL_NAME}
    except Exception:
        components["ocr_vllm"] = {"status": "down"}

    all_up = all(c.get("status") == "up" for c in components.values())
    return {
        "status": "healthy" if all_up else "degraded",
        "components": components,
    }
