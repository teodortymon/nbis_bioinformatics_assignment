import pytest
from httpx import AsyncClient

from main import app
import constants


# These tests can be flaky
# Would be great to have mocked api to test

# Integration tests make most sense when we control the whole unit
# Fun idea: to spin up external docker images of their

# TODO: Add mock tests
# TODO: implement thread pool
# Scenario 1: increase gradually
# Scenario 2: cold start
#


@pytest.mark.asyncio
async def test_all_restaurants():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(constants.RESTAURANTS_PATH)
    assert response.status_code == 200
    assert response.json() == constants.ALL_RESTAURANTS


@pytest.mark.asyncio
async def test_single_valid_restaurant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"{constants.RESTAURANTS_PATH}/{constants.RUDBECK_ID}")
    assert response.status_code == 200
    assert response.json() == constants.RUDBECK_DATA


@pytest.mark.asyncio
async def test_single_invalid_restaurant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"{constants.RESTAURANTS_PATH}/{constants.INVALID_RESTAURANT_ID}"
        )
    assert response.status_code == 400
    # assert response.json() == constants.RUDBECK_DATA


@pytest.mark.asyncio
async def test_relay_anything_all_restaurants():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"{constants.RELAY_ANYTHING}/{constants.RESTAURANTS_PATH}"
        )
    assert response.status_code == 200
    assert response.json() == constants.ALL_RESTAURANTS


@pytest.mark.asyncio
async def test_relay_anything_single_restaurant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"{constants.RELAY_ANYTHING}/{constants.RESTAURANTS_PATH}/{constants.RUDBECK_ID}/"
        )
    assert response.status_code == 200
    assert response.json() == constants.RUDBECK_DATA
