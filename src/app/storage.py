import json
from abc import ABC, abstractmethod
from typing import Dict, List

import redis


class Storage(ABC):
    """Abstract class for storage connectors."""

    @abstractmethod
    def __init__(self, url: str) -> None:
        self._url = url

    @abstractmethod
    def get(self, user_id: str) -> List[Dict[str, str]]:
        """Get list of items from storage."""
        raise NotImplementedError

    @abstractmethod
    def add(self, user_id: str, item: Dict) -> None:
        """Save item in storage."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """Delete user data from storage."""
        raise NotImplementedError


class RedisStorage(Storage):
    """Redis storage connector."""

    def __init__(self, url: str) -> None:
        super().__init__(url)
        self._redis = redis.from_url(self._url, decode_responses=True)

    def get(self, user_id: str, start=0, end=-1) -> List[Dict[str, str]]:
        """Return list of items from storage.

        Last saved item comes first.
        """
        return [
            json.loads(item)
            for item in self._redis.lrange(f"user:{user_id}", start, end)
        ]

    def add(self, user_id: str, item: Dict) -> None:
        """Dump item to string and push it on the head of the list."""
        self._redis.lpush(f"user:{user_id}", json.dumps(item))

    def delete(self, user_id: str) -> None:
        """Delete user data from storage."""
        self._redis.delete(f"user:{user_id}")
