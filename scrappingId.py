import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrappingCity(cityname, driver, restaurants, duplicatedlist):
    #하나의 행정동에 대한 모든 음식점 목록(최대100개)이 로딩된 html 소스 string 형태로 반환
    html = pageLoading(cityname, driver)
    #로딩된 html소스를 넘겨서 식당 id 및 이름 파싱해서 저장
    scrappingId(html, restaurants, duplicatedlist)
    #로딩된 html소스를 넘겨서 식당 위치 저장
    scrappingLocation(html, restaurants, duplicatedlist)

'''
위치 정보 파싱 함수, 식당 id 기반으로 lat,lng 값 저장
'''
def scrappingLocation(html, restaurants, duplicatedlist):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all(class_='Marker')
    for restaurantinfo in content:
        restaurantfullid = restaurantinfo['id']
        restaurantid = restaurantfullid[6:]
        lat = restaurantinfo['data-lat']
        lng = restaurantinfo['data-lng']
        searchresult = restaurants.get(restaurantid, 'NO_KEY')
        if searchresult != 'NO_KEY':
            restaurants[restaurantid]['lat'] = lat
            restaurants[restaurantid]['lng'] = lng


'''
식당 id 파싱 함수, 식당 id 기반으로 식당id&식당이름 저장
'''
def scrappingId(html, restaurants, duplicatedlist):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all(class_='PoiBlockContainer')
    for restaurantinfo in content:
        #가게 id 들어있는 텍스트가 'block'+'가게id'형식이라서 subString으로 'block'부분을 잘라주어야 함
        restaurantfullid = restaurantinfo.select_one('.PoiBlock')['id']
        restaurantid = restaurantfullid[5:]
        restaurantfullname = restaurantinfo.select_one('.InfoHeader > h2').string
        regex = re.compile('[0-9]{1,4}. ')
        regexres = regex.search(restaurantfullname)
        restaurantname = restaurantfullname[regexres.end():]

        #식당 정보를 저장하고 있는 dictionary에서
        searchresult = restaurants.get(restaurantid, 'NO_KEY')
        if searchresult == 'NO_KEY':
            restaurants[restaurantid] = {'id': restaurantid, 'name': restaurantname}
        else:
            duplicatedlist[restaurantid] = {'id': restaurantid, 'name': restaurantname}


'''
셀레니움사용해서 음식점 목록 최대 개수까지 스크롤 내려서 화면 로딩 후 html페이지 소스 반환
'''
def pageLoading(cityname, driver):
    # 검색창에 행정동 입력하는 url
    url = 'https://www.diningcode.com/list.dc?query=' + cityname
    driver.get(url)

    # 가게 리스트 DOM나올 때 까지 대기
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "PoiBlockContainer"))
        )
    finally:
        pass

    # beforeidx,nowidx 기준으로 스크롤 여부 결정 (beforeidx==nowidx 일 때에는 더 스크롤 할 가게들이 없다는 의미)
    beforeidx = 0
    nowidx = 0
    while True:
        restaurantblocks = driver.find_elements(By.CSS_SELECTOR, ".PoiList > ol > li")
        nowidx = len(restaurantblocks)
        if nowidx == beforeidx:
            break
        # 가게 리스트 맨 밑까지 스크롤 내리기
        driver.execute_script("arguments[0].scrollIntoView(true);", restaurantblocks[len(restaurantblocks) - 1])
        time.sleep(3)
        beforeidx = nowidx

    # BeautifulSoup으로 가게 정보 파싱(식당 id값, 식당 이름)
    html = driver.page_source
    return html


'''
음식점 정보 저장 함수, 현재는 텍스트 저장이지만 추후에 DB혹은 EXCEL로 변경할 예정
'''
def savedatas(restaurants, duplicatedlist):
    # 텍스트 파일 형태로 저장
    f = open("scrap.txt", 'w')
    for id in restaurants:
        f.write('id : ')
        f.write(restaurants[id]['id'])
        f.write(', name : ')
        f.write(restaurants[id]['name'])
        f.write(', location : {')
        f.write(restaurants[id]['lat'])
        f.write(', ')
        f.write(restaurants[id]['lng'])
        f.write('}')
        f.write('\n')
    f.close()
    f = open("duplicated.txt", 'w')
    for id in duplicatedlist:
        f.write('id ')
        f.write(duplicatedlist[id]['id'])
        f.write(' name ')
        f.write(duplicatedlist[id]['name'])
        f.write('\n')
    f.close()



def diningcodeScrapping():
    driver = webdriver.Chrome('chromedriver')
    #서울시 전체 행정 동 리스트
    citylist=['신사동','압구정동','논현동','청담동','삼성동','대치동','역삼동','도곡동','개포동',
              '일원동','수서동','세곡동','자곡동','율현동',
              '강일동','상일동','고덕동','명일동','암사동','천호동','성내동','길동','둔촌동','미아동',
              '번동','수유동','우이동',
              '염창동','등촌동','화곡동','내발산동','가양동','마곡동','외발산동','공항동','과해동','오곡동',
              '오쇠동','방화동','개화동',
              '봉천동','남현동','신림동',
              '중곡동','능동','구의동','광장동','자양동','화양동','군자동',
              '신도림동','구로동','가리봉동','고척동','개봉동','오류동','천왕동','항동','온수동','궁동',
              #금천구부터
              '가산동','독산동','시흥동','월계동','공릉동','하계동','중계동','상계동',
              '쌍문동','방학동','창동','도봉동',
              '신설동','제기동','전농동','답십리동','장안동','청량리동','회기동','휘경동','이문동',
              '노량진동','상도동','흑석동','사당동','대방동','신대방동',
              '아현동','도화동','용강동','대흥동','염리동','신수동','창전동','서교동','합정동','망원동','연남동','성산동'
              ,'상암동',
              '천연동','북아현동','대신동','연희동','홍제동','홍은동','남가좌동','북가좌동',
              '서초동','잠원동','반포동','방배동','양재동','내곡동',
              '하왕십리동','상왕십리동','마장동','사근동','행당동','응봉동','금호동1가','금호동2가','금호동3가','금호동4가'
              ,'옥수동','성수동1가','성수동2가','서울송정동','용답동',
              '성북동','삼선동','동선동','돈암동','안암동','보문동','정릉동','길음동','종암동','하월곡동','장위동','석관동',
              '풍납동','거여동','마천동','방이동','오금동','송파동','석촌동','삼전동','가락동','문정동','장지동','잠실동','신천동',
              '목동','신월동','신정동','영등포동','여의도동','당산동1가','당산동2가','당산동3가','당산동4가','당산동5가','당산동6가'
              ,'도림동','문래동1가','문래동2가','문래동3가','문래동4가','문래동5가','문래동6가','양평동1가','양평동2가','양평동3가'
              ,'양평동4가','양평동5가','양평동6가','신길동','대림동',
              '후암동','용산동1가','용산동2가','용산동3가','청파동1가','청파동2가','원효로1가','원효로2가','원효로3가','효창동'
              ,'용문동','한강로1가','한강로2가','한강로3가','이촌동','이태원동','한남동','서빙고동','보광동',
              '녹번동','불광동','갈현동','구산동','대조동','응암동','역촌동','신사동','증산동','수색동','진관동',
              '청운동','사직동','삼청동','부암동','평창동','무악동','교남동','가회동','종로1가','종로2가','종로3가','종로4가','종로5가'
              ,'종로6가','이화동','혜화동','창신동','숭인동',
              '소공동','화현동1가','태평로2가','남대문로1가','남대문로2가','남대문로3가','남대문로4가','남대문로5가'
              ,'회현동','명동','필동','장충동','광희동','을지로동','신당동','다산동','약수동','청구동','신당5동','동화동'
              ,'황학동','중림동',
              '면목동','상봉동','중화동','묵동','망우동','신내동']
    #테스트 용 citylist
    #citylist=['대방동','압구정동']

    #id값 중복 체크 후, restaurats에 dictionary형태로 가게 정보 저장
    #restaurants구조
    '''
    {
        '가게id1' : {
            'id' : '가게id',
            'name' : '가게이름',
            'lat' : 'lat값',
            'lng' : 'lng값'
        },
        '가게id2' : {
            'id' : '가게id',
            'name' : '가게이름',
            'lat' : 'lat값',
            'lng' : 'lng값'
        },   .....
    }
    '''
    #중복된 정보들은 duplicatedlist에 저장
    restaurants = {}
    duplicatedlist = {}
    #행정동 기준으로 순회하면서 스크래핑
    for cityname in citylist:
        scrappingCity(cityname, driver, restaurants, duplicatedlist)
    #데이터 저장
    savedatas(restaurants, duplicatedlist)
    driver.quit()


if __name__ == '__main__':
    diningcodeScrapping()

