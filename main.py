import time
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from open_time_crawl import crawl_open_time

if __name__ == '__main__':
    # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
    print('hello world')
    driver = webdriver.Chrome('chromedriver')
    # PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
    crawl_open_time(driver)
    driver.quit()
