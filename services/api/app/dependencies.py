from __future__ import annotations

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import User


async def get_default_user(
    db: AsyncSession = Depends(get_db),
) -> User:
    result = await db.execute(
        select(User).where(User.email == settings.default_user_email)
    )
    user = result.scalar_one_or_none()
    if user is not None:
        return user

    user = User(
        email=settings.default_user_email,
        display_name=settings.default_user_display_name,
    )
    db.add(user)
    try:
        await db.flush()
        return user
    except IntegrityError:
        await db.rollback()
        result = await db.execute(
            select(User).where(User.email == settings.default_user_email)
        )
        return result.scalar_one()
