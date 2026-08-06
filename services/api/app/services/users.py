from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def resolve_default_user(db: AsyncSession, email: str, display_name: str) -> User:
    from sqlalchemy import select
    from sqlalchemy.exc import IntegrityError

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is not None:
        return user

    user = User(email=email, display_name=display_name)
    db.add(user)
    try:
        await db.flush()
        return user
    except IntegrityError:
        await db.rollback()
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one()
