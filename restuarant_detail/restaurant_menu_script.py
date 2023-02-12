from abc import ABCMeta

from bs4 import BeautifulSoup, Tag

from core.abstract_script import AbstractScript


class RestaurantMenuScript(AbstractScript, metaclass=ABCMeta):
    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)

    def _get_result(self, el: Tag):
        if len(el.select_one(".Restaurant_MenuPrice")) == 0:
            return
        name = el.select_one(".Restaurant_Menu").text
        price = int(el.select_one(".Restaurant_MenuPrice").text[:-1].replace(',', ''))

        return {
            'name': name,
            'price': price,
            'isMainMenu': True if el.select_one(".icon") is not None else False
        }

    def _get_target_class(self) -> str:
        return '#div_detail>.menu-info>.Restaurant_MenuList>li'

    def get_property(self):
        return 'menus'
