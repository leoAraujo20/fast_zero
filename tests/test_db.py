from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, User


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
        'todo': [],
    }


@pytest.mark.asyncio
async def test_create_todo(session, user):
    todo = Todo(
        title='Test Todo',
        description='This is a test todo',
        state='todo',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    todo = await session.scalar(select(Todo))

    assert asdict(todo) == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'state': 'todo',
        'user_id': user.id,
    }


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user):
    todo = Todo(
        title='Test Todo',
        description='This is a test todo',
        state='todo',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    await session.refresh(user)

    user_db = await session.scalar(select(User).where(User.id == user.id))

    assert user_db.todo == [todo]
