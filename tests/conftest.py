import os
import sys
from collections.abc import Generator
from pathlib import Path

import fakeredis.aioredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# Test environment
os.environ.setdefault("APP_NAME", "Business Service Management API Test")
os.environ.setdefault("APP_VERSION", "0.0.1")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")


from app.core.redis import get_redis  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.database.base import Base  # noqa: E402
from app.database.session import get_db  # noqa: E402
from app.models.customer import Customer  # noqa: E402
from app.models.role import Role  # noqa: E402
from main import app  # noqa: E402


TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=TEST_ENGINE,
)


@pytest.fixture
def fake_redis_server():
    return fakeredis.aioredis.FakeRedis(decode_responses=True)


@pytest.fixture
def db_session(fake_redis_server) -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=TEST_ENGINE)

    session = TestSessionLocal()

    try:
        customer_role = Role(name="Customer")
        admin_role = Role(name="Administrator")

        session.add_all([customer_role, admin_role])
        session.flush()

        session.add(
            Customer(
                role_id=admin_role.id,
                first_name="Admin",
                last_name="User",
                email="admin@business.com",
                password_hash=hash_password("admin1234"),
            )
        )

        session.commit()

        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=TEST_ENGINE)

        if hasattr(app.state, "limiter"):
            app.state.limiter.reset()


@pytest.fixture
def client(
    db_session: Session,
    fake_redis_server,
) -> Generator[TestClient, None, None]:

    async def override_get_redis():
        return fake_redis_server

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def customer_auth(client: TestClient) -> dict:
    email = "customer_test@example.com"

    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Test",
            "last_name": "Customer",
            "email": email,
            "password": "password123",
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def admin_auth(client: TestClient) -> dict:
    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@business.com",
            "password": "admin1234",
        },
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }