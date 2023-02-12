from abc import ABC, abstractmethod
from selenium.webdriver.support import expected_conditions as EC
from typing import List

from bs4 import ResultSet, BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from abstract_script import AbstractScript


class AbstractScrapper(ABC):
    def __init__(self, url: str, target_class_for_waiting: str):
        self._target_class_for_waiting = target_class_for_waiting
        self._url = url
        self._driver = webdriver.Chrome('chromedriver')
        self._soup = self.__get_soup()
        self._scripts = self._get_scripts()

    @abstractmethod
    def _get_scripts(self) -> List[AbstractScript]:
        pass

    def _scrolling(self):
        pass

    def crawling(self):
        result = {}
        for script in self._scripts:
            result[script.get_property()] = script.crawl()
        return result

    def __del__(self):
        self._driver.quit()

    def __get_html(self):
        self.__loading_page()
        self._scrolling()
        return self._driver.page_source

    def __loading_page(self):
        self._driver.get(self._url)
        try:
            element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, self._target_class_for_waiting))
            )
        finally:
            pass

    def __get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.__get_html(), 'html.parser')
