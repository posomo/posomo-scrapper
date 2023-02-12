import decimal
from datetime import time, datetime
from enum import Enum
from typing import List


class Day(Enum):
    MON = '월'
    TUE = '화'
    WED = '수'
    THU = '목'
    FRI = '금'
    SAT = '토'
    SUN = '일'


class RestaurantTimeType(Enum):
    LAST_ORDER = 'LAST_ORDER'
    BREAK = 'BREAK'
    OPEN = 'OPEN'


class RestaurantLocation:
    def __init__(self, latitude: decimal, longitude: decimal, roadAddress: str):
        self.roadAddress = roadAddress
        self.latitude = latitude
        self.longitude = longitude


class RestaurantMenu:

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price


class RestaurantTime:

    def __init__(self, timeFrom: time, timeTo: time, days: List[Day], dtype: RestaurantTimeType):
        self.timeFrom = timeFrom
        self.timeTo = timeTo
        self.days = days
        self.dtype = dtype


class Restaurant:

    def __init__(self, rid: str, name: str, titleImageUrl: str, location: RestaurantLocation,
                 menus: List[RestaurantMenu], times: List[RestaurantTime]):
        self.rid = rid
        self.name = name
        self.titleImageUrl = titleImageUrl
        self.location = location
        self.menus = menus
        self.times = times
