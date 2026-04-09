from abc import ABC, abstractmethod

from relay.models.post import Post


class BaseFetcher(ABC):
    """Abstract base class for all source fetchers.

    Each fetcher (Reddit, HN, RSS) implements fetch() and returns
    a list of Post objects ready for dedup and classification.
    """

    @abstractmethod
    def fetch(self) -> list[Post]:
        """Fetch posts from the source.

        Returns:
            List of Post objects. May be empty if no new posts
            or if the source is unreachable.
        """
        ...

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Human-readable name for logging (e.g. 'Reddit', 'HackerNews')."""
        ...
