import json

import requests as requests

from city_list import city_list
from restuarant_detail.restaurant_detail_scrapper import RestaurantDetailScrapper

__base_url = 'https://im.diningcode.com/API/isearch/'


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.


def make_restaurant(restaurant):
    restaurant_result = {
        "rid": restaurant["v_rid"],
        "name": restaurant["nm"] + " " + restaurant["branch"] if restaurant["branch"] is not None else restaurant["nm"],
        "titleImageUrl": restaurant["image"],
        "location": {
            "roadAddress": restaurant["addr"],
            "latitude": restaurant["lat"],
            "longitude": restaurant["lng"]
        },
        "information": {
            "rating": restaurant["user_score"]
        }
    }
    detail = RestaurantDetailScrapper(restaurant["v_rid"]).crawling()
    restaurant_result.update(detail)
    print(restaurant_result)
    return restaurant


def get_restaurant_lists(query: str):
    from_i = 0
    result = get_list(query, from_i)
    restaurant_list = result["result_data"]["poi_section"]["list"]
    total_cnt = result["result_data"]["poi_section"]["total_cnt"]
    return_list = [make_restaurant(restaurant) for restaurant in restaurant_list]
    for i in range(20, total_cnt, 20):
        restaurant_list = get_list(query, i)["result_data"]["poi_section"]["list"]
        return_list.append([make_restaurant(restaurant) for restaurant in restaurant_list])


def get_list(query: str, from_i: int):
    head = {"User-Agent": "PostmanRuntime/7.30.0", 'Content-Type': 'application/x-www-form-urlencoded', "Accept": "*/*", "Origin": "https://www.diningcode.com", "Referer": "https://www.diningcode.com"}
    r = requests.post(__base_url, params={'query': query, 'from': str(from_i), 'size': str(20)}, headers=head).json()
    return r


if __name__ == '__main__':
    list(map(lambda query: get_restaurant_lists(query), city_list))
