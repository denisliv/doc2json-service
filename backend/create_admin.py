"""CLI script to create the initial admin user.

Usage:
    python create_admin.py admin changeme "Administrator"
"""

import asyncio
import sys

from sqlalchemy import select

from app.database import Base, async_session_factory, engine
from app.auth.service import hash_password
from app.auth.models import User

import app.documents.models  # noqa: F401
import app.document_types.models  # noqa: F401


async def create_admin(username: str, password: str, full_name: str | None = None):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as db:
        result = await db.execute(select(User).where(User.username == username))
        if result.scalar_one_or_none():
            print(f"User '{username}' already exists.")
            return

        user = User(
            username=username,
            password_hash=hash_password(password),
            full_name=full_name,
            role="admin",
            must_change_password=False,
        )
        db.add(user)
        await db.commit()
        print(f"Admin user created: {username}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py <username> <password> [full_name]")
        sys.exit(1)

    _username = sys.argv[1]
    _password = sys.argv[2]
    _name = sys.argv[3] if len(sys.argv) > 3 else None

    asyncio.run(create_admin(_username, _password, _name))
