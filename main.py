# 1. 사전규격공개 크롤링 모듈

#CMD
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

# chrome 최신 버전 설치하는 코드(작동 불가능)
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())
# C:\Anaconda3\envs\autorecipe 크롬 드라이버 위치 (버전이슈 생길 때 해당 버전에 맞는 chromedirver를 설치해서 저기 경로 안에 있는 chromedriver와 교체해주면 됨)

import pywinauto
from pywinauto import application
from pywinauto.application import Application

import pyperclip
import pyautogui

import time
from time import sleep

import readPreStandardDetail
import tools

tstart = time.time()
tenmean = 0.0
tencunt = 0
onemean = 0.0
onecunt = 0

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)# 위 cmd 명령어로 실행된 크롬 제어 권한을 획득


driver = tools.driverInit(driver)

def moveNextPage(driver):
    global tencunt
    tencunt += 1

    sleep(2)
    driver = tools.driverInit(driver)

    sleep(2)
    ele = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[1]')
    cur_page = int(ele.find_element(By.TAG_NAME, 'span').get_attribute("innerText"))  # 현재 페이지 넘버
    print('현재페이지', cur_page)
    cur_p1_ele_exist = False
    next_ele_exist = False

    for el in ele.find_elements(By.TAG_NAME,'a'):
        text = el.get_attribute("innerText")
        if text == str(cur_page + 1):
            cur_p1_ele = el
            cur_p1_ele_exist = True
            break
        elif text == '다음':
            next_ele = el
            next_ele_exist = True

    if cur_page % 10 != 0 and cur_p1_ele_exist == True:
        print('이동', cur_p1_ele.get_attribute("innerText"))
        cur_p1_ele.click()
    elif cur_page % 10 == 0 and next_ele_exist:
        print('이동', next_ele.get_attribute("innerText"))
        next_ele.click()
    else:
        print('마지막페이지 도달', cur_page, cur_p1_ele_exist, next_ele_exist)
        return False

    return True

# driver.find_element_by_name('name')
# driver.find_element_by_id('id')
# driver.find_element_by_xpath('/html/body/xpath')
# driver.find_element_by_class_name("lab_g lab_placeholder lab_txt").send_keys('prinn10@daum.net')

# driver.find_element_by_css_selector('#id > input.class')
# driver.find_element_by_class_name('class_name')
# driver.find_element_by_tag_name('h3')

#나라장터 접속
#driver.get('https://www.g2b.go.kr/pt/menu/selectSubFrame.do?framesrc=/pt/menu/frameTgong.do?url=https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCds=&bidNm=&searchDtType=1&fromBidDt=2022/03/27&toBidDt=2022/04/26&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&area=&regYn=Y&bidSearchType=1&searchType=1')
#
# sleep(2)
# driver.switch_to.frame(driver.find_element_by_name('sub'))
# sleep(2)
# driver.switch_to.frame(driver.find_element_by_name('left'))
# sleep(2)
# driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').click()
# sleep(2)
# driver.find_element_by_xpath('/html/body/div/ul/li[1]/ul/li[4]/a').click()
# sleep(2)


#driver.switch_to.default_content()
# #리스트박스 클릭
# Select(driver.find_element_by_id('swbizTgYn')).select_by_index(1)
#
# #검색
# driver.find_element_by_xpath('/html/body/div[2]/div[2]/form[1]/div[3]/div/a[1]').click()
# sleep(1)

#목록 정보 추출
while True:
    start = time.time()  # 시작 시간 저장

    tb1_keys = ['No.','등록번호','참조번호','품명','수요기관','사전규격공개일시','업체등록의견수','적합성여부']
    tb1info = tools.initListDict(tb1_keys)

    table = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/table')
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(7):
            body=value.find_elements(By.TAG_NAME,"td")[j]
            tb1info[tb1_keys[j]].append(body.text)

    # 목록 10개 순환 소스
    for i in range(1,11):
        driver = tools.driverInit(driver)
        driver.find_element(By.XPATH, '/html/body/div/div[2]/div/table/tbody/tr['+str(i)+']/td[4]/div/a').click()

        ##사전규격세부 읽고 처리##
        tb2info, tb3info, okng, mean, cunt = readPreStandardDetail.readPage(driver) # 페이지 정보 읽기
        onemean += mean
        onecunt += cunt

        print(tb2info)

        tools.writeTb2(tb2info)
        tools.writeTb3(tb3info)
        if okng == True:
            tb1info['적합성여부'].append('True')
        else:
            tb1info['적합성여부'].append('False')
        ######################

        driver.back()

    tools.writeTb1(tb1info)
    tenmean += time.time() - start
    print("10개 처리 시간 :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    if moveNextPage(driver) == False:
        break

print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간
print(tenmean , tencunt)
print("10개 평균 처리 시간", tenmean / tencunt)
print(onemean, onecunt)
print("파일 영업 적합성 검사 시간", onemean / onecunt)


