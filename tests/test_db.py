from datetime import UTC, datetime

import pytest

from relay.db.store import init_db, is_seen
from relay.db.models import PostRecord


@pytest.fixture
def session():
    """In-memory SQLite session for tests."""
    SessionLocal = init_db(":memory:")
    with SessionLocal() as s:
        yield s


class TestInitDb:
    def test_creates_tables(self, session):
        from sqlalchemy import inspect
        inspector = inspect(session.get_bind())
        table_names = inspector.get_table_names()
        assert "posts" in table_names
        assert "classifications" in table_names
        assert "ratings" in table_names
        assert "digest_queue" in table_names


class TestIsSeen:
    def test_unseen_post_returns_false(self, session):
        assert is_seen(session, "reddit:newpost") is False

    def test_seen_post_returns_true(self, session):
        record = PostRecord(
            id="reddit:abc123",
            source="reddit",
            title="Test post",
            url="https://reddit.com/test",
            created_at=datetime.now(UTC),
            fetched_at=datetime.now(UTC),
        )
        session.add(record)
        session.commit()
        assert is_seen(session, "reddit:abc123") is True

    def test_different_id_returns_false(self, session):
        record = PostRecord(
            id="reddit:abc123",
            source="reddit",
            title="Test post",
            url="https://reddit.com/test",
            created_at=datetime.now(UTC),
            fetched_at=datetime.now(UTC),
        )
        session.add(record)
        session.commit()
        assert is_seen(session, "reddit:different") is False
