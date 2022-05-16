import openpyxl as xl
import pandas as pd
from time import sleep
import os

# 셀레니움
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import zipfile

def writeTb1(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb1.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb2(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb2.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb3(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb3.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb4(tbinfo): # 크롤링 데이터 메타정보 저장함수
    pass

def initListDict(keys):
    ListDict = {}
    for key in keys:
        ListDict[key] = []
    return ListDict

def waitFileDownload(download_path):
    while True:
        file_list = os.listdir(download_path)
        all_check = False
        for file in file_list:
            if str(file).find('crdownload') != -1:
                sleep(0.3)
                print('다운로드 대기 중...')
                all_check = True
        if all_check == False:
            break

def driverInit(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.NAME, 'sub'))
    driver.switch_to.frame(driver.find_element(By.NAME, 'main'))
    # driver.implicitly_wait(5)

    return driver

def unzip(zip_file_name, download_path):
    with zipfile.ZipFile(os.path.join(download_path, zip_file_name), 'r') as zf:
        zipinfo = zf.infolist()
        for member in zipinfo:
            member.filename = member.filename.encode('cp437').decode('euc-kr')
            zf.extract(member, download_path)


def table_info_read(driver, table_xpath, table_keys, debug_mode = True): # 나라장터 테이블 양식을 크롤링하여 dic형태 반환하는 함수
    tb1info = initListDict(table_keys)

    table = driver.find_element(By.XPATH, table_xpath)
    tbody = table.find_element(By.TAG_NAME, "tbody")
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        th_list = []
        for th in tr.find_elements(By.TAG_NAME, "th"):
            print(th.get_attribute("innerText"))
            th_list.append(th.get_attribute("innerText"))
        td_list = []
        for td in tr.find_elements(By.TAG_NAME, "td"):
            print(td.get_attribute("innerText"))
            td_list.append(td.get_attribute("innerText"))

        for i in range(len(th_list)):
            tb1info[th_list[i]].append(td_list[i])

    return tb1info

