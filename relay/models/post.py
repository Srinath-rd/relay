from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel


class Post(BaseModel):
    """A single post fetched from any source."""

    id: str  # Unique across all sources: "reddit:abc123", "hn:42000000", "rss:url-hash"
    source: Literal["reddit", "hackernews", "rss"]
    title: str
    body: str | None = None
    url: str
    author: str | None = None
    score: int | None = None  # Upvotes, HN points, etc.
    created_at: datetime
    fetched_at: datetime = None  # Set by fetcher at fetch time

    # Source-specific metadata
    subreddit: str | None = None   # Reddit only
    feed_name: str | None = None   # RSS only
    comments_url: str | None = None

    def model_post_init(self, __context):
        if self.fetched_at is None:
            object.__setattr__(self, "fetched_at", datetime.now(UTC))

    @property
    def text_for_classification(self) -> str:
        """Combined text sent to the LLM for classification."""
        parts = [f"Title: {self.title}"]
        if self.subreddit:
            parts.append(f"Subreddit: r/{self.subreddit}")
        if self.feed_name:
            parts.append(f"Feed: {self.feed_name}")
        if self.body:
            # Truncate long bodies — LLM doesn't need the full text
            parts.append(f"Body: {self.body[:800]}")
        parts.append(f"URL: {self.url}")
        return "\n".join(parts)


class Classification(BaseModel):
    """Result of LLM classification for a post."""

    post_id: str
    bucket: Literal["very_interesting", "interesting", "good", "skip"]
    reasoning: str   # LLM's explanation — shown on dashboard
    confidence: float  # 0.0–1.0
    classified_at: datetime = None

    def model_post_init(self, __context):
        if self.classified_at is None:
            object.__setattr__(self, "classified_at", datetime.now(UTC))
