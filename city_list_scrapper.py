from abc import ABCMeta
from typing import List

from selenium.webdriver.common.by import By

from core.abstract_scrapper import AbstractScrapper
from core.abstract_script import AbstractScript
import time

from scripts.city_location_script import CityLocationScript


class CityListScrapper(AbstractScrapper, metaclass=ABCMeta):
    __base_url: str = "https://www.diningcode.com/list.dc?query="
    __target_class_for_waiting = "PoiBlockContainer"
    __target_block_class = ".PoiList > ol > li"

    def __init__(self, city_name: str):
        super().__init__(self.__base_url + city_name, self.__target_class_for_waiting)

    def _scrolling(self):
        before_idx = 0
        now_idx = 0
        while True:
            restaurant_blocks = super()._driver.find_elements(By.CSS_SELECTOR, self.__target_block_class)
            now_idx = len(restaurant_blocks)
            if now_idx == before_idx:
                break
            # 가게 리스트 맨 밑까지 스크롤 내리기
            super()._driver.execute_script("arguments[0].scrollIntoView(true);",
                                           restaurant_blocks[len(restaurant_blocks) - 1])
            time.sleep(3)
            before_idx = now_idx

    def _get_scripts(self) -> List[AbstractScript]:
        return [CityLocationScript(super()._soup)]
