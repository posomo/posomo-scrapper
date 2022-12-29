import time
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crawl_open_time(driver):
    driver.get("https://pcmap.place.naver.com/restaurant/1724662353/home")  # 네이버 신 지도

    arrow_selector = "#app-root > div > div > div > div:nth-child(6) > div > div:nth-child(2) > div " \
                     "> ul > li:nth-child(2) > div > a"
    arrow = driver.find_element(By.CSS_SELECTOR, arrow_selector)
    arrow.click()

    open_time_list_selector = "#app-root > div > div > div > div:nth-child(6) > div > " \
                              "div:nth-child(2) > div > ul > li:nth-child(n+2) > div > a > " \
                              "div"

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, open_time_list_selector))
        )
        time_list = driver.find_elements(By.CSS_SELECTOR, open_time_list_selector)
    finally:
        pass
    f = open("open_time_crawl.html", 'w')
    day_selector = "span > span"
    time_selector = "span > div"
    for element in time_list[1:]:
        day = element.find_element(By.CSS_SELECTOR, day_selector).get_attribute('innerHTML')
        time_string_list = element.find_element(By.CSS_SELECTOR, time_selector).get_attribute('innerHTML').replace("<span>", "").replace("</span>","").split('<br/>')
        for element in time_string_list:
            print(day + element)
            f.write(day+element)
    f.close()
