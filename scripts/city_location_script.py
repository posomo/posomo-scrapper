from abc import ABCMeta
from typing import TypeVar, Generic

from bs4 import BeautifulSoup, Tag

from core.abstract_script import AbstractScript
from restaurant import RestaurantLocation, Restaurant

T = TypeVar("T")


class CityLocationScript(AbstractScript, metaclass=ABCMeta):

    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)

    def _get_target_class(self) -> str:
        return 'Marker'

    def _get_result(self, el: Tag) -> T:
        restaurant_full_id = el['id']
        rid = restaurant_full_id[6:]
        location = RestaurantLocation(el['data-lat'], el['data-lng'])
        return Restaurant(rid=rid, location=location)
