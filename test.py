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
driver.implicitly_wait(3)

driver.switch_to.frame(driver.find_element_by_name('sub'))
driver.switch_to.frame(driver.find_element_by_name('main'))

# driver.find_element_by_name('name')
# driver.find_element_by_id('id')
# driver.find_element_by_xpath('/html/body/xpath')
# driver.find_element_by_class_name("lab_g lab_placeholder lab_txt").send_keys('prinn10@daum.net')

# driver.find_element_by_css_selector('#id > input.class')
# driver.find_element_by_class_name('class_name')
# driver.find_element_by_tag_name('h3')

