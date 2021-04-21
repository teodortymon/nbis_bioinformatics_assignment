from typing import Optional, Type, Union

import yaml
import logging
from fastapi import Depends, FastAPI, Path
from fastapi.exceptions import ValidationError
from socket import gaierror
from fastapi.responses import PlainTextResponse
from fastapi_cache import caches, close_caches  # type: ignore
from fastapi_cache.backends.base import BaseCacheBackend  # type: ignore
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend  # type: ignore
from httpx import AsyncClient, Response

from app import models
from app import messages

config = yaml.safe_load(open("config.yml"))
logger = logging.getLogger(__name__)

app = FastAPI()

# Set Redis as the cache
def redis_cache() -> Optional[BaseCacheBackend]:
    return caches.get(CACHE_KEY)


async def request_data(path: str) -> Response:
    async with AsyncClient() as ac:
        return await ac.get(path)


@app.get(f"/{config['RESTAURANTS_PATH']}", response_model=models.RestaurantList)
async def get_all_restaurants(
    cache: RedisCacheBackend = Depends(redis_cache),
):

    return await get_cache_or_request_with_model(
        "restaurant_list",
        models.RestaurantList,
        cache,
        f"{config['RELAY_SOURCE_URL']}/{config['RESTAURANTS_PATH']}",
    )


@app.get(
    f"/{config['RESTAURANTS_PATH']}/{{restaurant}}", response_model=models.Restaurant
)
async def get_single_restaurant(
    restaurant: str = Path(..., title="The ID of the restaurant you want to query"),
    cache: RedisCacheBackend = Depends(redis_cache),
):
    return await get_cache_or_request_with_model(
        restaurant,
        models.Restaurant,
        cache,
        f"{config['RELAY_SOURCE_URL']}/{config['RESTAURANTS_PATH']}/{restaurant}",
    )


async def get_cache_or_request_with_model(
    key: str,
    model: Type[models.BaseModel],
    cache: RedisCacheBackend,
    path: str,
) -> Union[models.BaseModel, PlainTextResponse]:
    cached_result = None
    cache_down = None
    try:
        cached_result = await cache.get(key)
        logger.debug(messages.CACHE_AVAILABLE)
    except Exception as ex:
        cache_down = True
        logger.debug(f"{messages.CACHE_UNAVAILABLE}\nErr: {repr(ex)}")

    try:
        if cached_result:
            logger.debug(messages.CACHE_HIT)
            return model.parse_raw(cached_result)
        else:
            response = await request_data(path)
            result = model.parse_raw(response.content)
            if not cache_down:
                await cache.set(key, result.json(), expire=config["CACHE_TTL"])
            return result

    except ValidationError as exc:
        return PlainTextResponse(
            messages.VALIDATION_FAIL,
            status_code=404,
        )


@app.get(f"/{config['RELAY_ANYTHING']}/{{query:path}}")
async def relay_anything(
    query: str,
    cache: RedisCacheBackend = Depends(redis_cache),
) -> str:
    return await get_cache_or_request_without_validation(
        f"relay_anything/{query}",
        cache,
        f"{config['RELAY_SOURCE_URL']}/{query}",
    )


async def get_cache_or_request_without_validation(
    key: str,
    cache: RedisCacheBackend,
    path: str,
) -> str:
    cached_result = None
    cache_down = None
    try:
        cached_result = await cache.get(key)
        logger.debug(messages.CACHE_AVAILABLE)
    except Exception as ex:
        cache_down = True
        logger.debug(f"{messages.CACHE_UNAVAILABLE}\nErr: {repr(ex)}")

    if cached_result:
        return cached_result
    else:
        response = await request_data(path)
        result = response.text
        if not cache_down:
            await cache.set(key, result, expire=config["CACHE_TTL"])
        return result


@app.on_event("startup")
async def on_startup() -> None:
    if redis_cache():
        caches.flush()
    rc = RedisCacheBackend("redis://redis:6379/?password=nbis_is_the_best")
    caches.set(CACHE_KEY, rc)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    try:
        await close_caches()
    except gaierror as ex:
        pass
