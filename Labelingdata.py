# cd C:\Program Files\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"
from collections import defaultdict

import os
print(os.getcwd())
# 셀레니움
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import pywinauto
from pywinauto import application
from pywinauto.application import Application

import pyperclip
import pyautogui

import time
from time import sleep

import readPreStandardDetail
import tools

# 개찰결과 데이터셋 수집 프로그램

# driver init
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
#
# driver = tools.driverInit(driver)

# 1. 검색 속성 설정 및 검색버튼 클릭

# 2. 리스트 순회
## 2.1. 리스트 정보 수집
## 2.1.1. 개찰 데이터 수집

#Move Next Page
def move_next_page():
    # 현재 페이지 출력
    # 마지막 페이지인지 확인 여부 출력
    pass

# 개찰결과 목록 리스트 정보 수집
def ListCrawling():
    readstart = time.time()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득

    driver = tools.driverInit(driver)

    # start = time.time()  # 시작 시간 저장
    #
    tb1_keys = ['업무','입찰공고번호','제입찰번호','공고명','수요기관','개찰일시','참가수','낙찰예정자','투찰금액/투찰금리','투찰률(%)','진행상황']
    tb1info = tools.initListDict(tb1_keys)

    table = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table')
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(11):
            body=value.find_elements(By.TAG_NAME,"td")[j]
            tb1info[tb1_keys[j]].append(body.text)

    #print(tb1info.items())
    list_len = len(tb1info['업무'])
    print("list",list_len, '읽어들인 시간 :', time.time() - readstart)  # 현재시각 - 시작시간 = 실행 시간
    u_len = 0 # 유찰 개수
    nu_len = 0 # 개찰완료, 재입찰 개수

    print(len(tb1info['업무']))

    # 목록 순환 소스
    for i in range(list_len):
        driver = tools.driverInit(driver)

        print('키 값', tb1info[tb1_keys[-1]][i])
        if tb1info[tb1_keys[-1]][i] == '유찰': # 진행상황 == 유찰
            print('skip 유찰')
            u_len += 1
            continue
        # 진행상황 == '개찰완료' or '재입찰'
        else:
            nu_len += 1
            driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table/tbody/tr['+str(i+1)+']/td[11]/div/a').click() # 해당 행이 개찰완료이면 개찰완료 버튼 클릭
            sleep(1)
            driver.back()
            sleep(1)
    print('페이지 순회 완료')
    print('해당 페이지 리스트 개수', list_len, '중 유찰 개수', u_len, '개찰완료or재입찰 개수', nu_len, '입니다')
    pass

# 입찰결과 목록 정보 수집
def ResultCrawling():
    readstart = time.time()
    # driver init 나중에 전역변수로 통일하는 작업 필요할 듯... 개발중에는 디버그 편한대로
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    pass

if __name__ == '__main__':
    tstart = time.time()
    ListCrawling()
    ResultCrawling()
    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간