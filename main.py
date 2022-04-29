#CMD
# cd C:\Program Files\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tools
import readPreStandardDetail
import pywinauto
from pywinauto import application
from pywinauto.application import Application

import pyperclip
import pyautogui

from time import sleep
from selenium.webdriver.support.select import Select

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
driver.implicitly_wait(5)

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
driver.switch_to.frame(driver.find_element_by_name('sub'))
driver.switch_to.frame(driver.find_element_by_name('main'))
# #리스트박스 클릭
# Select(driver.find_element_by_id('swbizTgYn')).select_by_index(1)
#
# #검색
# driver.find_element_by_xpath('/html/body/div[2]/div[2]/form[1]/div[3]/div/a[1]').click()
# sleep(1)

#목록 정보 추출
tb1_keys = ['No.','등록번호','참조번호','품명','수요기관','사전규격공개일시','업체등록의견수','적합성여부']
tb1info = tools.initListDict(tb1_keys)

table = driver.find_element_by_xpath('/html/body/div/div[2]/div/table')
tbody = table.find_element_by_tag_name("tbody")
rows = tbody.find_elements_by_tag_name("tr")
for i, value in enumerate(rows):
    for j in range(7):
        body=value.find_elements_by_tag_name("td")[j]
        tb1info[tb1_keys[j]].append(body.text)

# 목록 10개 순환 소스
driver.switch_to.default_content()
for i in range(1,11):
    driver.switch_to.frame(driver.find_element_by_name('sub'))
    driver.switch_to.frame(driver.find_element_by_name('main'))
    driver.find_element_by_xpath('/html/body/div/div[2]/div/table/tbody/tr['+str(i)+']/td[4]/div/a').click()

    ##사전규격세부 읽고 처리##
    tb2info, tb3info, okng = readPreStandardDetail.readPage(driver) # 페이지 정보 읽기
    tools.writeTb2(tb2info)
    tools.writeTb3(tb3info)
    if okng == True:
        tb1info['적합성여부'].append('True')
    else:
        tb1info['적합성여부'].append('False')
    ######################

    driver.back()
    driver.switch_to.default_content()

tools.writeTb1(tb1info)

### page read
# tb2info, tb3info, okng = readPreStandardDetail.readPage(driver) # 페이지 정보 읽기
# tools.writeTb2(tb2info)
# tools.writeTb3(tb3info)
