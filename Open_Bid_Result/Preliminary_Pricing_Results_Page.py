# 예비가격 산정결과 페이지 크롤링
# 2. 물품 입찰공고 상세
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
import readHWP
import Monitoring

def Init(): # 각종 요소 초기화
    ## table names
    table_names = ['입찰공고정보', '기초금액 정보']

    ## table elements
    table_element_list = tools.initListDict(table_names)

    ## info_tables : table dic 'table_name', table_keys'
    info_tables = tools.initListDict(table_names)
    info_tables['입찰공고정보'].append(['입찰공고번호', '참조번호', '입찰분류', '재입찰번호', '공고명', '낙찰자선정적용기준', '실제 개찰일시', '예가범위', '기초금액기준\n상위갯수','정렬기준','복수예비가격\n작성시각'])
    # info_tables['예비가격 정보제공'].append(['입찰공고번호', '금액', '추첨횟수'])
    info_tables['기초금액 정보'].append(['예정가격', '기초금액'])

    return table_names, table_element_list, info_tables

def search_table_xpath(driver, table_element_list, info_tables): # table elements 탐색
    tables_xpath = driver.find_elements(By.TAG_NAME, 'table')  # 리스트 타입의 테이블을 읽어들임

    print(len(tables_xpath))
    if len(tables_xpath) == 2:
        table_element_list['입찰공고정보'].append(tables_xpath[0])
        table_element_list['기초금액 정보'].append(tables_xpath[1])
    elif len(tables_xpath) == 3:
        table_element_list['입찰공고정보'].append(tables_xpath[0])
        # table_element_list['예비가격 정보제공'].append(tables_xpath[1])
        table_element_list['기초금액 정보'].append(tables_xpath[2])

    for key, val in table_element_list.items():
        print('---------------------',key)
        print(val)

    return table_element_list


def Preliminary_Pricing_Results_Crawling(driver, table_names, table_element_list, info_tables, pri_value): # 해당 페이지 정보 크롤링
    tb_info = []
    for i, table_name in enumerate(table_names):
        if table_name == '입찰공고정보' or table_name == '기초금액 정보':  # table type 1(th td th td)
            tb_info.append(tools.advanced_table_info_read(table_element_list[table_name][0], info_tables[table_name][0]))
        # elif table_name == '예비가격 정보제공':  # table type 2 (list table)
        #     tb_info.append(tools.adadvanced_table1_info_read(table_element_list[table_name], info_tables[table_name][0]))
        print('table_name : ', table_name)
        print(tb_info[i])

    # 3.2 csv write
    for i, tb in enumerate(tb_info):
        tools.insert_value(tb, '예비가격산정결과'+str(i+1), pri_value)


def Preliminary_Pricing_Results_Page_Crawling(driver, pri_value):
    tstart = time.time()
    monitoring = Monitoring.monitoring()
    table_names, table_element_list, info_tables = Init()
    table_element_list = search_table_xpath(driver, table_element_list, info_tables)
    Preliminary_Pricing_Results_Crawling(driver, table_names, table_element_list, info_tables, pri_value)
    monitoring.update('pre_pri', time.time() - tstart, print_type='updated_element')

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    driver.find_element(By.XPATH, '/html/body/div/div[2]/form[1]/div[2]/table/tbody/tr[5]/td[2]/div/a').click()
    while len(driver.window_handles) < 2:
        print('페이지 로딩중... 예비가격 산정결과')
        sleep(0.1)
    driver.switch_to.window(driver.window_handles[-1])  # 최근 열린 탭으로 전환

    Preliminary_Pricing_Results_Page_Crawling(driver, '')
