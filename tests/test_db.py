from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(
        username='alice',
        password='alice123',
        email='alice@gmail.com',
    )

    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.username == new_user.username)
    )

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'alice123',
        'email': 'alice@gmail.com',
        'created_at': new_user.created_at,
        'updated_at': new_user.updated_at,
    }
