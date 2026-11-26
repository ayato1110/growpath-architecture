from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.core.errors import ApiError


@lru_cache
def get_engine(database_url: str, pool_size: int, max_overflow: int) -> Engine:
    if not database_url:
        raise ApiError(
            503,
            "DATABASE_NOT_CONFIGURED",
            "Database belum dikonfigurasi",
            "DATABASE_URL belum diisi di environment backend.",
        )
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_recycle=300,
        connect_args={"connect_timeout": 10, "prepare_threshold": None},
    )


@lru_cache
def _session_factory(
    database_url: str, pool_size: int, max_overflow: int
) -> sessionmaker[Session]:
    return sessionmaker(
        bind=get_engine(database_url, pool_size, max_overflow),
        autoflush=False,
        expire_on_commit=False,
    )


def get_db() -> Iterator[Session]:
    settings = get_settings()
    factory = _session_factory(
        settings.database_url, settings.db_pool_size, settings.db_max_overflow
    )
    session = factory()
    try:
        yield session
    finally:
        session.close()
