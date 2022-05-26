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

import csv

import tools
import Monitoring

import Bid_Announcement_Detail_Page
import Bid_Result_Detail_Page
import Bid_Result_List_Page
import Preliminary_Pricing_Results_Page

class main:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
        self.driver = tools.driverInit(self.driver)
        self.nu_len = 0 # 개찰완료 개수
        self.monitoring = Monitoring.monitoring()
        self.date = '2022/01/03'
        self.dataset_path = 'C:\\pycharm\\source\\autoNarajangteo\\Open_Bid_Result\\Dataset'
        self.tb1_keys = ['업무', '입찰공고번호', '재입찰번호', '공고명', '수요기관', '개찰일시', '참가수', '낙찰예정자', '투찰금액/투찰금리', '투찰률(%)','진행상황']

    def completed_date_check(self):  # 해당 날짜 크롤링 여부를 확인
        try:
            completed_page_list = []
            f = open(os.path.join(self.dataset_path, 'completed_page.csv'), 'r', encoding='UTF8')
            rdr = csv.reader(f)
            for line in rdr:
                completed_page_list.append(line[1])
            f.close()
            if self.date in completed_page_list:
                return True
            else:
                return False
        except: # 파일이 존재하지 않을 경우
            return False

    def open_date_select_page(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, 'sub'))
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, 'left'))
        self.driver.find_element(By.XPATH, '/html/body/div/ul/li[1]/ul/li[6]/a').click()
        self.driver = tools.driverInit(self.driver)

    def select_date(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(executable_path='chromedriver',
                                       options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
        self.driver = tools.driverInit(self.driver)
        print(self.date, '크롤링 시작')
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "container")))
        print('페이지 로딩 완료, 입찰 정보 검색')
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[1]').clear()  # 시작일 입력
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[1]').send_keys(self.date)  # 시작일 입력
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[2]').clear()  # 종료일 입력
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[4]/input[2]').send_keys(self.date)  # 종료일 입력
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/a[1]').click()  # 검색

    def total_process(self, type):
        # 1. 날짜 초기화
        while True:
            if type == 'resume':
                self.date = tools.calculate_date(self.date, 1)  # 날짜 빼기 연산
                res = self.completed_date_check()
                if self.completed_date_check():  # 1.1. 해당 날짜 크롤링 여부를 확인
                    print('해당 날짜는 이미 크롤링 되었으므로 다음 날짜로 넘어갑니다')
                    continue
                # 1.2 날짜 선택 및 검색
                self.select_date()
            else:
                type = 'asd'
            while True:
                readstart = time.time()
                # 2. 한 페이지의 리스트를 순회
                tb1info = tools.initListDict(self.tb1_keys)
                table = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/table')))
                if table.text.find('검색된 데이터가 없습니다.') != -1:
                    print('검색된 데이터가 없습니다.')
                    self.open_date_select_page()
                    self.monitoring.update('lis_cra', time.time() - readstart, print_type='updated_element')
                    break
                else:
                    ## 2.1 개찰결과 목록 크롤링 및 저장
                    print('페이지 로딩 완료, 개찰결과 목록')
                    tbody = table.find_element(By.TAG_NAME, "tbody")
                    rows = tbody.find_elements(By.TAG_NAME, "tr")
                    for i, value in enumerate(rows):
                        for j in range(11):
                            body = value.find_elements(By.TAG_NAME, "td")[j]
                            tb1info[self.tb1_keys[j]].append(body.text)
                    tools.writeTb5(tb1info, 'lis_cra')
                    self.monitoring.update('lis_cra', time.time() - readstart, print_type='updated_element')

                    ## 2.2 개찰결과 목록 순환
                    for i in range(len(tb1info['업무'])):
                        self.driver = tools.driverInit(self.driver)

                        if tb1info[self.tb1_keys[-1]][i] in ['유찰', '재입찰', '상세조회']:  # 진행상황 == 유찰
                            print('skip 유찰, 재입찰, 상세조회')

                        else:  # 진행상황 == '개찰완료'
                            toustart = time.time()
                            ## 2.3. 물품입찰공고상세 이동
                            self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/table/tbody/tr[' + str(
                                i + 1) + ']/td[11]/div/a').click()  # 해당 행이 개찰완료이면 개찰완료 버튼 클릭
                            table = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/form[1]/div[2]/table')))
                            print('페이지 로딩 완료, 물품 개찰결과 상세조회')
                            ### 2.3.1. 물품 개찰결과 상세조회 페이지 크롤링
                            Bid_Result_Detail_Page.Bid_Result_Detail_Page_Crawling(self.driver, tb1info['입찰공고번호'][i])

                            ## 2.4. 예비가격 산정결과 이동
                            self.driver.find_element(By.XPATH,'/html/body/div/div[2]/form[1]/div[2]/table/tbody/tr[5]/td[2]/div/a').click()
                            while len(self.driver.window_handles) < 2:
                                print('페이지 로딩중... 예비가격 산정결과')
                                sleep(0.1)
                            self.driver.switch_to.window(self.driver.window_handles[-1])  # 최근 열린 탭으로 전환

                            if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "div"))).text.find('협상에 의한 계약의 예비가격 및 예정가격은 최종낙찰자 선정 이후에 공개됩니다.') != -1:
                                print('최종낙찰자 미선정으로 정보추출 불가능..')
                            else:
                                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "container")))
                                print('페이지 로딩 완료, 예비가격 산정결과')
                                ### 2.4.1. 예비가격 산정결과 페이지 크롤링
                                Preliminary_Pricing_Results_Page.Preliminary_Pricing_Results_Page_Crawling(self.driver,tb1info['입찰공고번호'][i])

                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[-1])
                            self.driver = tools.driverInit(self.driver)
                            ### 2.4.2. ###

                            ## 2.5. 공고상세 이동
                            self.driver.find_element(By.CLASS_NAME, 'btn_mdl').click()  # 공고상세 페이지로 이동
                            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "table_info")))
                            print('페이지 로딩 완료, 물품 입찰공고 상세')

                            ### 2.5.1 물품 입찰공고 상세 페이지 크롤링
                            Bid_Announcement_Detail_Page.Bid_Announcement_Detail_Page_Crawling(self.driver,tb1info['입찰공고번호'][i])

                            ## 2.6. 개찰결과 목록으로 복귀
                            self.driver.back()
                            self.driver.back()

                            self.monitoring.update('tot_cou', time.time() - toustart, print_type='all_element')
                            print('list 탐색 ', i + 1, len(tb1info['업무']))

                    # 3. 다음 페이지로 이동 이동
                    if tools.check_final_page(self.driver) == False:
                        self.driver = tools.driverInit(self.driver)
                        div = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[3]')))
                        cur_page = div.find_element(By.TAG_NAME, 'strong')
                        print('현재 페이지', cur_page.get_attribute("innerText"), '다음페이지 이동')
                        div.find_elements(By.TAG_NAME, 'a')[-1].click()
                    else:  ## 3.1. 현재 페이지가 마지막 페이지면 날짜 선택창으로 이동
                        self.driver = self.open_date_select_page()
                        break
            print('date 저장완료', self.date)
            tools.writeTb5({'date': [self.date]}, 'completed_page', save_path='C:\\pycharm\\source\\autoNarajangteo\\Open_Bid_Result\\Dataset') # 4. 해당 일자는 크롤링 완료됬다고 기록
            print('페이지 순회 완료')

if __name__ == '__main__':
    tstart = time.time()
    main = main()
    main.total_process(type='resume')
    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간