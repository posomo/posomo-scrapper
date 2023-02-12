from restuarant_detail.restaurant_detail_scrapper import RestaurantDetailScrapper

# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    result = RestaurantDetailScrapper("sD0Gl5p2yBoD").crawling()
    print(result)
