import time
from abc import ABCMeta
from datetime import time
from typing import List

from bs4 import BeautifulSoup, Tag

from core.abstract_script import AbstractScript
from restaurant import Day, RestaurantTimeType


def get_time(time_string: str):
    string_split = time_string.strip().split(' ')
    hour = int(string_split[1][:-1])
    minute = 0
    if len(string_split) > 2:
        minute = int(string_split[2][:-1])
    if string_split[0] == '오후':
        hour += 12
    if string_split[0] == '자정':
        hour = 23
        minute = 59
    return time(hour=hour, minute=minute)


class RestaurantTimeScript(AbstractScript, metaclass=ABCMeta):
    __days: List[Day] = [Day.SUN, Day.MON, Day.TUE, Day.WED, Day.THU, Day.FRI, Day.SAT]

    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)

    def __is_24(self, text : str):
        return text.find("24시간 영업") != -1

    def _get_result(self, el: Tag):
        day_strings = el.select_one(".l-txt").text.split(' ')
        day = day_strings[-1]
        if day == "휴무일":
            return
        dtype = RestaurantTimeType.OPEN
        if day_strings[0] == '쉬는시간':
            dtype = RestaurantTimeType.BREAK
        days = self._get_days_array(day)
        text = el.select_one(".r-txt").text.replace('\"', '').strip()
        if el.select_one(".r-txt>span") is not None:
            text = text.split('(')[0].strip()
        time_range = text.split(' - ')
        timeFrom = time(hour=0, minute=0) if self.__is_24(text) else get_time(time_range[0])
        timeTo = time(hour=23, minute=59) if self.__is_24(text) else get_time(time_range[1])
        return {
            'days': days,
            'dtype': dtype,
            'timeFrom': timeFrom,
            'timeTo': timeTo
        }

    def get_property(self):
        return 'times'

    def _get_days_array(self, day: str):
        days = []

        if day.find("매일") != -1:
            return self.__days
        elif day.find("-") != -1:
            index = day.find("-")
            start = self.__days.index(Day(day[index - 1]))
            end = self.__days.index(Day(day[index + 1]))
            days = self.__days[start:end + 1]
        if day.find('토') != -1:
            days.append(Day.SAT)
        if day.find('일') != -1 and day.find('요일') == -1:
            days.append(Day.SUN)
        if day.find('주말') != -1:
            days.append(Day.SAT)
            days.append(Day.SUN)
        return days

    def _get_target_class(self) -> str:
        return '#div_detail>.busi-hours>ul>li'
