import openpyxl as xl
import pandas as pd
from time import sleep
import os
import re
# 셀레니움
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import zipfile
from pathlib import Path
import shutil
from datetime import datetime, timedelta

def writeTb5(tbinfo, filename, save_path='C:\\pycharm\\source\\autoNarajangteo\\Open_Bid_Result\\Dataset'): # 물품입찰공고상세
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv(os.path.join(save_path, filename+'.csv'), mode='a', header=False, index=True, encoding='utf-8-sig')

def initListDict(keys):
    ListDict = {}
    for key in keys:
        ListDict[key] = []
    return ListDict

def calculate_date(date, num):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    now = datetime(year, month, day)
    now = now - timedelta(days = num)

    strnow = str(now)[0:10]
    return strnow[0:4]+'/'+strnow[5:7]+'/'+strnow[8:10]

def waitFileDownload(download_path):
    while True:
        file_list = os.listdir(download_path)
        if len(file_list) == 0:
            print('다운로드된 파일이 없음...')
            sleep(0.3)
            continue
        all_check = False
        for file in file_list:
            if str(file).find('crdownload') != -1 or str(file).find('.tmp') != -1:
                sleep(0.3)
                print('다운로드 대기 중...')
                all_check = True
        if all_check == False:
            break

def driverInit(driver):
    driver.switch_to.default_content()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "sub")))
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
            if value.find_element(By.TAG_NAME,"td").text in ['공개된 정보가 없습니다.','자료없음','첨부된 파일이 없습니다.']: # 데이터가 없을 경우
                tb1info[table_keys[j]].append('')
            else: # 데이터가 있을 경우
                body=value.find_elements(By.TAG_NAME,"td")[j]
                tb1info[table_keys[j]].append(body.text)

    return tb1info

# table type 2: 첫행만 추출
def advanced_table2_info_read(table_element, table_keys): # 나라장터 테이블 양식을 크롤링하여 dic형태 반환하는 함수
    tb1info = initListDict(table_keys)
    tbody = table_element.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(len(table_keys)):
            if value.find_element(By.TAG_NAME,"td").text in ['공개된 정보가 없습니다.','자료없음','첨부된 파일이 없습니다.']: # 데이터가 없을 경우
                tb1info[table_keys[j]].append('')
            else: # 데이터가 있을 경우
                body=value.find_elements(By.TAG_NAME,"td")[j]
                tb1info[table_keys[j]].append(body.text)
        if i == 1:
            break

    return tb1info

def extract_number(num_str): # num_str 문자열에서 숫자반 추출하여 반환
    # numbers = re.sub(r'[^0-9]', '', num_str)
    numbers = None
    numbers = re.findall("\d+.\d+",num_str)
    numbers += re.findall("\d+",num_str)
    if numbers != []:
        for i in range(len(numbers)):
            if numbers[i].find('.') != -1:
                numbers[i] = float(numbers[i])
            else:
                numbers[i] = int(numbers[i])
        return numbers
    else:
        return None

def insert_value(tb_info, table_name, pri_value=None, save_path='C:\\pycharm\\source\\autoNarajangteo\\Open_Bid_Result\\Dataset'):
    # tb의 요소 중 가장 긴 길이를 추출
    tb_lenth = 0
    for key in tb_info.keys():
        if tb_lenth < len(tb_info[key]):
            tb_lenth = len(tb_info[key])

    # 결측치를 모두 ''로 채우고 모든 배열들의 길이를 동일하게 맞춤
    for key in tb_info.keys():
        while len(tb_info[key]) != tb_lenth:
            tb_info[key].append('')

    if pri_value != None: # pri_value 값 추가
        # pri_value가 존재하는 경우
        if '입찰공고번호' in tb_info.keys():
            tb_info['입찰공고번호'].clear()
        else: # 존재하지 않는 경우
            tb_info['입찰공고번호'] = []

        while len(tb_info['입찰공고번호']) != tb_lenth:
            tb_info['입찰공고번호'].append(pri_value)

    db = pd.DataFrame(tb_info, columns=tb_info.keys())
    db.to_csv(os.path.join(save_path, table_name+'.csv'), index=True, mode='a', encoding='utf-8-sig')

    return tb_info

def move_file(src_file_path, download_path = None, dst_dir_path='C:\\pycharm\\source\\autoNarajangteo\\Open_Bid_Result\\debug'):
    if download_path == None:
        try:
            shutil.move(src_file_path,dst_dir_path)
        except:
            os.remove(src_file_path)
    else:
        try:
            shutil.move(os.path.join(download_path, src_file_path),dst_dir_path)
        except:
            os.remove(os.path.join(download_path, src_file_path))

def del_dow(tb_info, index): # tb_info : dictionary type , value : list type
    for key in tb_info.keys():
        del tb_info[key][index]
    return tb_info

def check_final_page(driver): # 해당 페이지가 마지막 페이지인지 검사하는 기능 제공
    driver = driverInit(driver)
    div = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[3]")))
    text_info = div.text
    if text_info.find('다음') == -1 and text_info.find('끝') == -1 and text_info.find('더보기') == -1:
        print('마지막 페이지')
        return True
    else:
        return False

if __name__ == '__main__':
    # num = extract_number('대상으로 예정가격 이하로서 예정가격 대비  80.1243%이상 최저가 입찰자 순으로 <조달청 물품구매 적격심사 세부기준>에 따라 평가하여 종합평점이  이상인 자를 낙찰자로 결정')
    # print(num)

    waitFileDownload('C:\\Users\\정희운\\Downloads')