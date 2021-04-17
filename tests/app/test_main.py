import pytest
import yaml
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.main import app
from tests import test_constants

config = yaml.safe_load(open("config.yml"))


@pytest.fixture()
async def httpxclient():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac


@pytest.mark.asyncio
async def test_all_restaurants(httpxclient):
    response = await httpxclient.get(config["RESTAURANTS_PATH"])
    assert response.status_code == 200
    assert response.json()
    assert "restaurants" in response.text


@pytest.mark.asyncio
async def test_single_valid_restaurant(httpxclient):
    response = await httpxclient.get(
        f"{config['RESTAURANTS_PATH']}/{test_constants.RUDBECK_ID}"
    )
    assert response.status_code == 200
    assert response.json()
    assert "Rudbeck" in response.text


@pytest.mark.asyncio
async def test_single_invalid_restaurant(httpxclient):
    response = await httpxclient.get(
        f"{config['RESTAURANTS_PATH']}/{test_constants.INVALID_RESTAURANT_ID}"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_relay_anything_all_restaurants(httpxclient):
    response = await httpxclient.get(
        f"{config['RELAY_ANYTHING']}/{config['RESTAURANTS_PATH']}"
    )
    assert response.status_code == 200
    assert response.json()
    assert "restaurants" in response.text


@pytest.mark.asyncio
async def test_relay_anything_single_restaurants(httpxclient):
    response = await httpxclient.get(
        f"{config['RELAY_ANYTHING']}/{config['RESTAURANTS_PATH']}/{test_constants.RUDBECK_ID}/"
    )
    assert response.status_code == 200
    assert response.json()
    assert "Rudbeck" in response.text
