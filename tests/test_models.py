from datetime import UTC, datetime

import pytest

from relay.models.post import Classification, Post


def make_post(**kwargs) -> Post:
    defaults = dict(
        id="reddit:abc123",
        source="reddit",
        title="Claude 4 released with 10x improvement",
        url="https://reddit.com/r/MachineLearning/abc123",
        created_at=datetime.now(UTC),
    )
    defaults.update(kwargs)
    return Post(**defaults)


class TestPost:
    def test_basic_creation(self):
        post = make_post()
        assert post.id == "reddit:abc123"
        assert post.source == "reddit"
        assert post.fetched_at is not None  # Auto-set

    def test_text_for_classification_with_subreddit(self):
        post = make_post(subreddit="MachineLearning", body="Some details here")
        text = post.text_for_classification
        assert "Title:" in text
        assert "Subreddit: r/MachineLearning" in text
        assert "Some details here" in text

    def test_text_for_classification_truncates_long_body(self):
        post = make_post(body="x" * 1000)
        text = post.text_for_classification
        # Body should be truncated to 800 chars
        assert len([line for line in text.split("\n") if line.startswith("Body:")][0]) <= 810

    def test_text_for_classification_rss(self):
        post = make_post(source="rss", feed_name="OpenAI Blog", subreddit=None)
        text = post.text_for_classification
        assert "Feed: OpenAI Blog" in text

    def test_optional_fields_default_none(self):
        post = make_post()
        assert post.body is None
        assert post.author is None
        assert post.score is None
        assert post.subreddit is None

    def test_invalid_source_raises(self):
        with pytest.raises(Exception):
            make_post(source="twitter")


class TestClassification:
    def test_basic_creation(self):
        c = Classification(
            post_id="reddit:abc123",
            bucket="very_interesting",
            reasoning="Breaking AI release",
            confidence=0.95,
        )
        assert c.bucket == "very_interesting"
        assert c.classified_at is not None

    def test_invalid_bucket_raises(self):
        with pytest.raises(Exception):
            Classification(
                post_id="reddit:abc123",
                bucket="meh",
                reasoning="whatever",
                confidence=0.5,
            )

    @pytest.mark.parametrize("bucket", ["very_interesting", "interesting", "good", "skip"])
    def test_all_valid_buckets(self, bucket):
        c = Classification(
            post_id="test:1",
            bucket=bucket,
            reasoning="test",
            confidence=0.8,
        )
        assert c.bucket == bucket
