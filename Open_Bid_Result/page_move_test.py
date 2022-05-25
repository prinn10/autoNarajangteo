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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from time import sleep

import tools
import Monitoring

import Bid_Announcement_Detail_Page
import Bid_Result_Detail_Page
import Bid_Result_List_Page
import Preliminary_Pricing_Results_Page

from datetime import datetime, timedelta

def completed_date_check(date): # 해당 날짜 크롤링 여부를 확인
    date = tools.calculate_date(date, 1)  # 날짜 빼기 연산
    completed_page_list = []
    f = open(os.path.join(dataset_path, 'completed_page'), 'r', encoding='UTF8')
    rdr = csv.reader(f)
    for line in rdr:
        completed_page_list.append(line[0])
    f.close()
    if date in completed_page_list:
        return True
    else:
        return False

def open_date_select_page(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.NAME, 'sub'))
    driver.switch_to.frame(driver.find_element(By.NAME, 'left'))
    driver.find_element(By.XPATH, '/html/body/div/ul/li[1]/ul/li[6]/a').click()
    return tools.driverInit(driver)

def total_process(driver):
    #모든 월별 페이지를 순환

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    # 1. 날짜 초기화
    date = '2018/01/07'
    while True:
        date = tools.calculate_date(date, 1) # 날짜 빼기 연산
        if completed_date_check(date):  # 1.1. 해당 날짜 크롤링 여부를 확인
            print('해당 날짜는 이미 크롤링 되었으므로 다음 날짜로 넘어갑니다')
            continue

        # 1.2 날짜 선택 및 검색
        print(date,'크롤링 시작')
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "container")))
        print('페이지 로딩 완료, 입찰 정보 검색')
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[1]').clear() # 시작일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[1]').send_keys(date) # 시작일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[2]').clear() # 종료일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[2]').send_keys(date) # 종료일 입력
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/a[1]').click() # 검색
        while True:
            # 2. 한 페이지의 리스트를 순회
            tb1_keys = ['업무','입찰공고번호','재입찰번호','공고명','수요기관','개찰일시','참가수','낙찰예정자','투찰금액/투찰금리','투찰률(%)','진행상황']
            tb1info = tools.initListDict(tb1_keys)

            table = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/table')))
            if table.text.find('검색된 데이터가 없습니다.') != -1:
                driver = open_date_select_page(driver)

                # 4. 날짜 변경 후 1.로 돌아감
                date = tools.calculate_date(date, 1)
                break
            else:
                print('페이지 로딩 완료, 개찰결과 목록')
                tbody = table.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")
                for i, value in enumerate(rows):
                    for j in range(11):
                        body=value.find_elements(By.TAG_NAME,"td")[j]
                        tb1info[tb1_keys[j]].append(body.text)

                # 목록 순환 소스
                for i in range(len(tb1info['업무'])-2,len(tb1info['업무'])):
                    driver = tools.driverInit(driver)

                    if tb1info[tb1_keys[-1]][i] in ['유찰', '재입찰', '상세조회']: # 진행상황 == 유찰
                        print('skip 유찰, 재입찰, 상세조회')

                    else:# 진행상황 == '개찰완료'
                        # 물품입찰공고상세 이동
                        driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table/tbody/tr['+str(i+1)+']/td[11]/div/a').click() # 해당 행이 개찰완료이면 개찰완료 버튼 클릭
                        table = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/form[1]/div[2]/table')))
                        print('페이지 로딩 완료, 물품 개찰결과 상세조회')

                        # 예비가격 산정결과 이동
                        driver.find_element(By.XPATH,'/html/body/div/div[2]/form[1]/div[2]/table/tbody/tr[5]/td[2]/div/a').click()
                        while len(driver.window_handles) < 2:
                            print('페이지 로딩중... 예비가격 산정결과')
                            sleep(0.1)
                        driver.switch_to.window(driver.window_handles[-1])  # 최근 열린 탭으로 전환

                        if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "div"))).text.find('협상에 의한 계약의 예비가격 및 예정가격은 최종낙찰자 선정 이후에 공개됩니다.') != -1:
                            print('최종낙찰자 미선정으로 정보추출 불가능..')
                        else:
                            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "container")))
                            print('페이지 로딩 완료, 예비가격 산정결과')

                        driver.close()
                        driver.switch_to.window(driver.window_handles[-1])

                        driver = tools.driverInit(driver)

                        # 공고상세 이동
                        driver.find_element(By.CLASS_NAME, 'btn_mdl').click()  # 공고상세 페이지로 이동
                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "table_info")))
                        print('페이지 로딩 완료, 물품 입찰공고 상세')

                        driver.back()
                        driver.back()

                    print('list 탐색 ', i+1, len(tb1info['업무']))

                if tools.check_final_page(driver) == False:
                    driver = tools.driverInit(driver)
                    div = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[3]')))
                    cur_page = div.find_element(By.TAG_NAME, 'strong')
                    print('현재 페이지', cur_page.get_attribute("innerText"), '다음페이지 이동')
                    div.find_elements(By.TAG_NAME, 'a')[-1].click()
                else: # 현재 페이지가 마지막 페이지면
                    # 3. 날짜 선택창으로 이동
                    driver = open_date_select_page(driver)
                    break
        tools.writeTb5({ 'date' : [date]}, 'completed_page', save_path='C:\\pycharm\\source\\autoNarajangteo\\Open_Bid_Result\\Dataset')

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    total_process(driver)

