from typing import Dict, List, Union, Type
from pydantic import BaseModel


class RestaurantDetails(BaseModel):
    location: str
    map_url: str
    menu: List[Dict[str, str]]
    title: str
    url: str


class Restaurant(BaseModel):
    restaurant: RestaurantDetails


class RestaurantListDetails(BaseModel):
    campus: str
    identifier: str
    menu_url: str
    name: str
    osm: str
    url: str


class RestaurantList(BaseModel):
    restaurants: List[RestaurantListDetails]


# anyIORestaurantModelType = Union[Type[Restaurant], Type[RestaurantList]]
# anyIORestaurantModelType = Union[Restaurant, RestaurantList]
