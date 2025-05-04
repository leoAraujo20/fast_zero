import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_user_model(session):
    new_user = User(username='test', password='test', email='test@gmail.com')

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    user = await session.scalar(select(User).where(User.username == 'test'))

    assert user.id == 1
