#CMD
# cd C:\Program Files\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import test
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
# table = driver.find_element_by_xpath('/html/body/div/div[2]/div/table')
# tbody = table.find_element_by_tag_name("tbody")
# rows = tbody.find_elements_by_tag_name("tr")
#
# y = []
# for i, value in enumerate(rows):
#     x = []
#     for j in range(7):
#         body=value.find_elements_by_tag_name("td")[j]
#         x.append(body.text)
#     y.append(x)
#
# for i in range(10):
#     for j in range(7):
#         print(y[i][j],end='  ')
#     print()

tbinfo, okng = test.readPage(driver) # 페이지 정보 읽기
print(tbinfo)
print(okng)