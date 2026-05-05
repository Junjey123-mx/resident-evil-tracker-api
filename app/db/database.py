from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.core.config import get_settings

_settings = get_settings()

# pool_pre_ping=True detects stale connections before use
engine = create_engine(
    _settings.database_url,
    echo=False,
    pool_pre_ping=True,
)


def get_engine():
    return engine


def get_session() -> Generator[Session, None, None]:
    # Intended as a FastAPI dependency — yields one session per request
    with Session(engine) as session:
        yield session
