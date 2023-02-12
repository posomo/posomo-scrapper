from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from bs4 import BeautifulSoup, ResultSet, PageElement, Tag



class AbstractScript(ABC):

    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._content = soup.select(self._get_target_class())

    def crawl(self) -> list:
        result = []
        for el in self._content:
            target = self._get_result(el)
            result.append(target)
        return result

    @abstractmethod
    def _get_result(self, el: Tag):
        pass

    @abstractmethod
    def get_property(self):
        pass
    @abstractmethod
    def _get_target_class(self) -> str:
        pass
