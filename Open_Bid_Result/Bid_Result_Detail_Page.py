# f. 물품 개찰결과 상세조회
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

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
driver = tools.driverInit(driver)


# 물품개찰결과상세조회 페이지
def bid_res_crawling(): # 입찰결과 테이블 크롤링 함수
    # 1. 입찰결과 테이블 키 값 리스트 정의
    bid_res_keys = ['입찰공고번호', '참조번호', '공고명', '공고기관', '수요기관', '공고담당자', '집행관', '실제개찰일시', '복수예비가 및\n예정가격', '적격심사결과', '유의사항']

    sleep(2)
    table = driver.find_element(By.XPATH, '/html/body/div/div[2]/form[1]/div[2]/table')
    tbody = table.find_element(By.TAG_NAME, "tbody")
    tb2info = tools.initListDict(bid_res_keys)
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        th_list = []
        for th in tr.find_elements(By.TAG_NAME, "th"):
            th_list.append(th.get_attribute("innerText"))
        td_list = []
        for td in tr.find_elements(By.TAG_NAME, "td"):
            td_list.append(td.get_attribute("innerText"))
        for i in range(len(th_list)):
            tb2info[th_list[i]].append(td_list[i])

    # 테이블 정보 출력
    print(bid_res_keys)
    for i in range(len(tb2info[bid_res_keys[0]])):
        for key in bid_res_keys:
            if key != '유의사항':
                print(tb2info[key][i], end=' ')
        print()


def open_bid_rank_crawling(): # 개찰결과순위 테이블 크롤링 함수
    # 1. 개찰순위 테이블 키 값 리스트 정의
    open_bid_keys = ['순위', '사업자등록번호', '업체명', '대표자', '투찰금액', '투찰률(%)', '추첨번호', '투찰일시', '비고']

    tb1info = tools.initListDict(open_bid_keys)

    table = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table')
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(len(open_bid_keys)):
            body=value.find_elements(By.TAG_NAME,"td")[j]
            # print(body.text) # debug
            tb1info[open_bid_keys[j]].append(body.text)

    # 테이블 정보 출력
    print(open_bid_keys)
    for i in range(len(tb1info[open_bid_keys[0]])):
        for key in open_bid_keys:
            print(tb1info[key][i], end=' ')
        print()

def Bid_Result_Detail_Page_Crawling():
    bid_res_crawling()
    open_bid_rank_crawling()

if __name__ == '__main__':
    tstart = time.time()
    Bid_Result_Detail_Page_Crawling()
    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간