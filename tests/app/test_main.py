import pytest
import logging
import yaml
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.main import app
from app import messages
from tests import test_constants

config = yaml.safe_load(open("config.yml"))
logger = logging.getLogger(__name__)


def pytest_generate_tests(metafunc):
    if "client" in metafunc.fixturenames:
        metafunc.parametrize(
            "client, cache_log_msg",
            [
                (
                    pytest.lazy_fixture("httpxclient_with_cache"),
                    messages.CACHE_AVAILABLE,
                ),
                (
                    pytest.lazy_fixture("httpxclient_without_cache"),
                    messages.CACHE_UNAVAILABLE,
                ),
            ],
        )


@pytest.fixture()
async def httpxclient_with_cache(caplog):
    async with LifespanManager(app):
        caplog.set_level(logging.DEBUG)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac


@pytest.fixture()
async def httpxclient_without_cache(caplog, cache_log_msg):
    caplog.set_level(logging.DEBUG)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_all_restaurants(client, cache_log_msg, caplog):
    response = await client.get(config["RESTAURANTS_PATH"])
    assert response.status_code == 200
    assert response.json()
    assert test_constants.VALID_MANY_RESTAURANTS_STRING in response.text
    assert cache_log_msg in caplog.text


@pytest.mark.asyncio
async def test_single_valid_restaurant(client, cache_log_msg, caplog):
    response = await client.get(
        f"{config['RESTAURANTS_PATH']}/{test_constants.VALID_RESTAURANT_ID}"
    )
    assert response.status_code == 200
    assert response.json()
    assert test_constants.VALID_RESTAURANT_TITLE in response.text
    assert cache_log_msg in caplog.text


@pytest.mark.asyncio
async def test_single_invalid_restaurant(client, cache_log_msg, caplog):
    response = await client.get(
        f"{config['RESTAURANTS_PATH']}/{test_constants.INVALID_RESTAURANT_ID}"
    )
    assert response.status_code == 404
    assert cache_log_msg in caplog.text


@pytest.mark.asyncio
async def test_relay_anything_all_restaurants(client, cache_log_msg, caplog):
    response = await client.get(
        f"{config['RELAY_ANYTHING']}/{config['RESTAURANTS_PATH']}"
    )
    assert response.status_code == 200
    assert response.json()
    assert test_constants.VALID_MANY_RESTAURANTS_STRING in response.text
    assert cache_log_msg in caplog.text


@pytest.mark.asyncio
async def test_relay_anything_single_restaurants(client, cache_log_msg, caplog):
    response = await client.get(
        f"{config['RELAY_ANYTHING']}/{config['RESTAURANTS_PATH']}/{test_constants.VALID_RESTAURANT_ID}"
    )
    assert response.status_code == 200
    assert response.json()
    assert test_constants.VALID_RESTAURANT_TITLE in response.text
    assert cache_log_msg in caplog.text
