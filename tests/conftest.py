import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture
def client(session):
    def override_get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client

    app.dependency_overrides = {}


@pytest.fixture(scope='session')
def engine():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    return engine


@pytest_asyncio.fixture
async def session(engine):

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def mock_db_time(session): ...


@pytest_asyncio.fixture
async def user(session):
    password = 'test123'
    user = User(
        username='test',
        password=get_password_hash(password),
        email='test@test.com',
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password
    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'test345'
    user = User(
        username='test2',
        password=get_password_hash(password),
        email='test2@test.com',
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )
    return response.json().get('access_token')
