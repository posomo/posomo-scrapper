from abc import ABCMeta
from typing import List

from core.abstract_scrapper import AbstractScrapper
from core.abstract_script import AbstractScript
from restuarant_detail.restaurant_menu_script import RestaurantMenuScript
from restuarant_detail.restaurant_time_script import RestaurantTimeScript


class RestaurantDetailScrapper(AbstractScrapper, metaclass=ABCMeta):
    def __init__(self, id: str):
        super().__init__("https://www.diningcode.com/profile.php?rid=" + id, "Restaurant_Menu")

    def _get_scripts(self) -> List[AbstractScript]:
        return []


if __name__ == '__main__':
    result = RestaurantDetailScrapper("sD0Gl5p2yBoD").crawling()
    print(result)
