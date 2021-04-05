from typing import Optional, Type

from fastapi import FastAPI, Path, Depends
from fastapi_cache import caches, close_caches  # type: ignore
from fastapi_cache.backends.base import BaseCacheBackend  # type: ignore
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend  # type: ignore
from httpx import AsyncClient

import constants
import models

# TODO: Add more explanatory error messages
# TODO: Separate mock test from the production config
# TODO: Add mypy and pytest as CI/CD


app = FastAPI()


# Set Redis as the cache
def redis_cache() -> Optional[BaseCacheBackend]:
    return caches.get(CACHE_KEY)


@app.get(f"/{constants.RESTAURANTS_PATH}", response_model=models.RestaurantList)
async def get_all_restaurants(
    cache: RedisCacheBackend = Depends(redis_cache),
):

    return await get_cache_or_request_with_model(
        "restaurant_list",
        models.RestaurantList,
        cache,
        f"{constants.RELAY_SOURCE_URL}/{constants.RESTAURANTS_PATH}",
    )


async def get_cache_or_request_with_model(
    key: str,
    model: Type[models.BaseModel],
    cache: RedisCacheBackend,
    path: str,
) -> models.BaseModel:
    cached_result = await cache.get(key)

    if cached_result:
        return model.parse_raw(cached_result)
    else:
        async with AsyncClient() as ac:
            response = await ac.get(path)
            result = model.parse_raw(response.content)
            await cache.set(key, result.json(), expire=constants.ONE_HOUR)
            return result


async def get_cache_or_request_without_validation(
    key: str,
    cache: RedisCacheBackend,
    path: str,
) -> str:
    cached_result = await cache.get(key)

    if cached_result:
        return cached_result
    else:
        async with AsyncClient() as ac:
            response = await ac.get(path)
            result = response.text
            await cache.set(key, result, expire=constants.ONE_HOUR)
            return result


@app.get(
    f"/{constants.RESTAURANTS_PATH}/{{restaurant}}", response_model=models.Restaurant
)
async def get_single_restaurant(
    restaurant: str = Path(..., title="The ID of the restaurant you want to query"),
    cache: RedisCacheBackend = Depends(redis_cache),
):
    return await get_cache_or_request_with_model(
        restaurant,
        models.Restaurant,
        cache,
        f"{constants.RELAY_SOURCE_URL}/{constants.RESTAURANTS_PATH}/{restaurant}",
    )


# Using :path parameter directly from Starlette
@app.get(f"/{constants.RELAY_ANYTHING}/{{query:path}}")
async def relay_anything(
    query: str,
    cache: RedisCacheBackend = Depends(redis_cache),
) -> str:
    return await get_cache_or_request_without_validation(
        f"relay_anything/{query}",
        cache,
        f"{constants.RELAY_SOURCE_URL}/{query}",
    )


@app.on_event("startup")
async def on_startup() -> None:
    rc = RedisCacheBackend("redis://redis:6379/?password=nbis_is_the_best")
    caches.set(CACHE_KEY, rc)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await close_caches()
