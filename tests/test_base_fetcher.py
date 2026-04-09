from datetime import UTC, datetime

import pytest

from relay.fetchers.base import BaseFetcher
from relay.models.post import Post


class ConcreteFetcher(BaseFetcher):
    """Minimal concrete implementation for testing the interface."""

    @property
    def source_name(self) -> str:
        return "TestSource"

    def fetch(self) -> list[Post]:
        return [
            Post(
                id="test:1",
                source="reddit",
                title="Test post",
                url="https://example.com",
                created_at=datetime.now(UTC),
            )
        ]


class TestBaseFetcher:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BaseFetcher()

    def test_concrete_fetcher_works(self):
        fetcher = ConcreteFetcher()
        posts = fetcher.fetch()
        assert len(posts) == 1
        assert posts[0].id == "test:1"

    def test_source_name(self):
        fetcher = ConcreteFetcher()
        assert fetcher.source_name == "TestSource"

    def test_fetch_returns_list(self):
        fetcher = ConcreteFetcher()
        result = fetcher.fetch()
        assert isinstance(result, list)
