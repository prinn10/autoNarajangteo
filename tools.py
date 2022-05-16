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

def writeTb5(tbinfo, filename): # 물품입찰공고상세
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv(filename+'.csv', mode='a', header=False, index=True, encoding='utf-8-sig')
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

# table type 1: tr th tr th
def advanced_table_info_read(table_element, table_keys): # 나라장터 테이블 양식을 크롤링하여 dic형태 반환하는 함수
    tb1info = initListDict(table_keys)

    tbody = table_element.find_element(By.TAG_NAME, "tbody")
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        th_list = []
        for th in tr.find_elements(By.TAG_NAME, "th"):
            th_list.append(th.get_attribute("innerText"))
        td_list = []
        for td in tr.find_elements(By.TAG_NAME, "td"):
            td_list.append(td.get_attribute("innerText"))
        for i in range(len(th_list)):
            tb1info[th_list[i]].append(td_list[i])

    return tb1info

# table type 2: list
def advanced_table1_info_read(table_element, table_keys): # 나라장터 테이블 양식을 크롤링하여 dic형태 반환하는 함수
    tb1info = initListDict(table_keys)
    tbody = table_element.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(len(table_keys)):
            if value.find_element(By.TAG_NAME,"td").text == '공개된 정보가 없습니다.' or value.find_element(By.TAG_NAME,"td").text == '자료없음': # 데이터가 없을 경우
                tb1info[table_keys[j]].append('')
            else: # 데이터가 있을 경우
                body=value.find_elements(By.TAG_NAME,"td")[j]
                tb1info[table_keys[j]].append(body.text)

    return tb1info
