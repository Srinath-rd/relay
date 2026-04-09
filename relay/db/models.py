from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PostRecord(Base):
    """All posts seen — used for deduplication and history."""

    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # "reddit:abc123"
    source: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str | None] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str | None] = mapped_column(String)
    score: Mapped[int | None] = mapped_column(Integer)
    subreddit: Mapped[str | None] = mapped_column(String)
    feed_name: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class ClassificationRecord(Base):
    """LLM classification output for each post."""

    __tablename__ = "classifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    bucket: Mapped[str] = mapped_column(String, nullable=False)  # very_interesting | interesting | good | skip
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    classified_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class RatingRecord(Base):
    """User feedback — confirmed or corrected bucket for a post.

    Injected as few-shot examples into future classification prompts.
    """

    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    post_title: Mapped[str] = mapped_column(Text, nullable=False)  # Denormalized for prompt injection
    bucket: Mapped[str] = mapped_column(String, nullable=False)    # User-confirmed bucket
    rated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))


class DigestQueueRecord(Base):
    """Posts queued for the next email digest."""

    __tablename__ = "digest_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    bucket: Mapped[str] = mapped_column(String, nullable=False)  # interesting | good
    queued_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
