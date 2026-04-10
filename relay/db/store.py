from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from relay.db.models import Base


def init_db(db_path: str) -> sessionmaker:
    """Initialize the SQLite database and return a session factory.

    Creates all tables if they don't exist. Safe to call on every startup.

    Args:
        db_path: Path to the SQLite file (e.g. "relay.db")

    Returns:
        A sessionmaker bound to the engine.
    """
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def is_seen(session: Session, post_id: str) -> bool:
    """Return True if this post has already been processed."""
    from relay.db.models import PostRecord
    return session.get(PostRecord, post_id) is not None
