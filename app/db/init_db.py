"""
Initialize the PostgreSQL database by creating all tables registered in
SQLModel's metadata.
"""

from sqlmodel import SQLModel

from app.db.database import get_engine

# Import all table=True models so SQLModel registers their metadata before
# create_all() is called. Omitting any import means that table won't be created.
from app.modules.archive_entries.archive_entry_model import ArchiveEntry  # noqa: F401
from app.modules.personal_ratings.rating_model import Rating  # noqa: F401
from app.modules.activity_logs.activity_model import ActivityLog  # noqa: F401


def init_database() -> None:
    """Create all SQLModel-registered tables on the configured PostgreSQL engine.

    Safe to run multiple times — CREATE TABLE IF NOT EXISTS is the effective
    behaviour because SQLModel.metadata.create_all() skips tables that already
    exist in the target database.
    """
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def main() -> None:
    init_database()
    print("Database tables created successfully.")


if __name__ == "__main__":
    main()
