import json

import pytest
import redis

from app.storage import RedisStorage


@pytest.fixture
def url():
    return "redis://localhost:6379/"


@pytest.fixture
def db(url):
    return RedisStorage(url)


@pytest.fixture
def native_redis(url):
    return redis.from_url(url)


@pytest.fixture()
def user_id():
    return "999999"


@pytest.fixture
def places():
    return [
        {
            "Title": f"Shop {i}",
            "Address": f"Shop {i} Address",
            "Photo": f"photo_{i}_url",
        }
        for i in range(1, 21)
    ]


def test_add_saves_place(db, native_redis, user_id, places):
    user_key = "user:" + user_id
    db.add(user_id, places[0])

    result = native_redis.lindex(user_key, 0)

    assert json.loads(result) == places[0]


def test_get_returns_list_of_dicts(db, native_redis, user_id, places):
    user_key = "user:" + user_id
    for place in places[:5]:
        native_redis.lpush(user_key, json.dumps(place))

    result = db.get(user_id, 0, 4)

    assert list(reversed(result)) == places[:5]


def test_delete_removes_user_data(db, native_redis, user_id, places):
    user_key = "user:" + user_id
    for place in places[:5]:
        native_redis.lpush(user_key, json.dumps(place))

    db.delete(user_id)

    assert native_redis.exists(user_key) == 0
