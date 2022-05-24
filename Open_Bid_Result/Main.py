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

import time
from time import sleep

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

    def move_next_page(self):
        sleep(1)
        div = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]')
        a_list = div.find_elements(By.TAG_NAME, 'a')[-1].click()
        cur_page = div.find_element(By.TAG_NAME, 'strong')
        print('현재 페이지', cur_page.get_attribute("innerText"), '다음페이지 이동')
        sleep(1)

    # 개찰결과 목록 리스트 정보 수집
    def ListCrawling(self):
        readstart = time.time()
        self.driver = tools.driverInit(self.driver)

        tb1_keys = ['업무','입찰공고번호','재입찰번호','공고명','수요기관','개찰일시','참가수','낙찰예정자','투찰금액/투찰금리','투찰률(%)','진행상황']
        tb1info = tools.initListDict(tb1_keys)

        table = self.driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table')
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for i, value in enumerate(rows):
            for j in range(11):
                body=value.find_elements(By.TAG_NAME,"td")[j]
                tb1info[tb1_keys[j]].append(body.text)

        tools.writeTb5(tb1info, 'lis_cra')

        self.monitoring.update('lis_cra', time.time() - readstart, print_type='updated_element')
        # 목록 순환 소스
        for i in range(len(tb1info['업무'])):
            self.driver = tools.driverInit(self.driver)

            if tb1info[tb1_keys[-1]][i] == '유찰' or tb1info[tb1_keys[-1]][i] == '재입찰' or tb1info[tb1_keys[-1]][i] == '상세조회': # 진행상황 == 유찰
                print('skip 유찰, 재입찰, 상세조회')
                continue

            else:# 진행상황 == '개찰완료'
                self.nu_len += 1
                self.driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table/tbody/tr['+str(i+1)+']/td[11]/div/a').click() # 해당 행이 개찰완료이면 개찰완료 버튼 클릭
                sleep(2)

                Bid_Result_Detail_Page.Bid_Result_Detail_Page_Crawling(self.driver, tb1info['입찰공고번호'][i]) # 물품 개찰결과 상세조회 페이지 크롤링
                Preliminary_Pricing_Results_Page.Preliminary_Pricing_Results_Page_Crawling(self.driver, tb1info['입찰공고번호'][i]) # 예비가격 산정결과 페이지 크롤링
                self.driver = tools.driverInit(self.driver)
                self.driver.find_element(By.CLASS_NAME, 'btn_mdl').click() # 공고상세 페이지로 이동
                sleep(1)
                Bid_Announcement_Detail_Page.Bid_Announcement_Detail_Page_Crawling(self.driver, tb1info['입찰공고번호'][i]) # 공고상세 페이지 크롤링

                self.driver.back()
                sleep(1) # 이부분 속도 수정
                self.driver.back()
                sleep(1)

                self.monitoring.update('tot_cou', time.time() - readstart, print_type='all_element')

        print('페이지 순회 완료')
        print('해당 페이지 리스트 개수', len(tb1info['업무']), '중 개찰완료 개수', self.nu_len)

    def total_process(self):
        while True:
            self.ListCrawling()
            self.move_next_page()
            sleep(2)

if __name__ == '__main__':
    tstart = time.time()
    main = main()
    main.total_process()
    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간