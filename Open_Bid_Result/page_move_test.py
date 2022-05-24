# cd C:\Program Files\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"
from collections import defaultdict

import os
# 셀레니움
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import time
from time import sleep

import tools
import Monitoring

import Bid_Announcement_Detail_Page
import Bid_Result_Detail_Page
import Bid_Result_List_Page
import Preliminary_Pricing_Results_Page

from datetime import datetime, timedelta

start_date = '20180108'
end_date = '20220108'

def save_resume_info(): # 크롤링 완료된 기간 정보 저장
    pass

def crawling_resume(type='prev'): # 이전 종료 시점부터 다시 크롤링 시작하는 기능 제공
    if type == 'prev': # start_date로 부터 이전 일자를 크롤링
        pass
    elif type == 'prev': # end_date로 부터 이후 일자를 크롤링
        pass
    pass

def check_final_page(driver): # 해당 페이지가 마지막 페이지인지 검사하는 기능 제공
    div = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]')
    text_info = div.text
    if text_info.find('다음') == -1 and text_info.find('끝') == -1:
        return True
    else:
        return False
    pass

def select_date(driver):
    day = '2012/06/08'
    while True:
        # prev일 때

        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[1]').clear() # 시작일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[1]').send_keys(day) # 시작일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[2]').clear() # 종료일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[2]').send_keys(day) # 종료일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/a[1]').click() # 검색
        sleep(2)

        while True:
            sleep(1)
            div = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]')
            if check_final_page(driver):
                break
            a_list = div.find_elements(By.TAG_NAME, 'a')[-1].click()
            cur_page = div.find_element(By.TAG_NAME, 'strong')
            print('현재 페이지', cur_page.get_attribute("innerText"), '다음페이지 이동')
            sleep(1)

        move_bid_res_page(driver)
        day = calculate_date(date, 1)
    pass

def move_bid_res_page(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.NAME, 'sub'))
    driver.switch_to.frame(driver.find_element(By.NAME, 'left'))

    driver.find_element(By.XPATH, '/html/body/div/ul/li[1]/ul/li[6]/a').click()

    driver = tools.driverInit(driver)

def test(driver):
    check_final_page(driver)
    # select_date(driver)
    # move_bid_res_page(driver)
    pass

def total_process(driver):
    #모든 월별 페이지를 순환

    while True:
        # 1. 날짜 선택 및 검색
        # 2. 한 페이지의 리스트를 순회
            # 물품입찰공고상세
            # 물품개찰결과상세
            # 예비가격 산정결과
        # 모든 페이지 리스트 순회 끝

        # 3. 날짜 선택창으로 이동
        # 4. 날짜 변경 후 1.로 돌아감


def calculate_date(date, num):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    print(year, month, day)
    now = datetime(year, month, day)
    now = now - timedelta(days = num)

    strnow = str(now)[0:10]
    print(strnow)
    return strnow[0:4]+'/'+strnow[5:7]+'/'+strnow[8:10]

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)
    tstart = time.time()
    test(driver)
    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간