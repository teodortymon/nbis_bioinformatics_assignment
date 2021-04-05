import pytest
from httpx import AsyncClient

import config
from main import app
import test_constants


# The integration tests below can be flaky
# so it would be great to add a mocked api for testing

# Fun idea: package and spin up docker containers of the other API
# and make e2e tests :)

# TODO: Refactor tests to use redis cache


@pytest.mark.asyncio
async def test_all_restaurants():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(config.RESTAURANTS_PATH)
    assert response.status_code == 200
    assert response.json()


@pytest.mark.asyncio
async def test_single_valid_restaurant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"{config.RESTAURANTS_PATH}/{test_constants.RUDBECK_ID}")
    assert response.status_code == 200
    assert response.json()


@pytest.mark.asyncio
async def test_single_invalid_restaurant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"{config.RESTAURANTS_PATH}/{test_constants.INVALID_RESTAURANT_ID}"
        )
    assert response.status_code == 400
    # assert response.json() == constants.RUDBECK_DATA


@pytest.mark.asyncio
async def test_relay_anything_all_restaurants():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"{config.RELAY_ANYTHING}/{config.RESTAURANTS_PATH}"
        )
    assert response.status_code == 200
    assert response.json() == test_constants.ALL_RESTAURANTS


@pytest.mark.asyncio
async def test_relay_anything_single_restaurant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"{config.RELAY_ANYTHING}/{config.RESTAURANTS_PATH}/{test_constants.RUDBECK_ID}/"
        )
    assert response.status_code == 200
    assert response.json() == test_constants.RUDBECK_DATA
