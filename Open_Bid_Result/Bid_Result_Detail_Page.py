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
import Monitoring

# 물품개찰결과상세조회 페이지
def bid_res_crawling(driver, pri_value): # 입찰결과 테이블 크롤링 함수
    # 1. 입찰결과 테이블 키 값 리스트 정의
    bid_res_keys = ['입찰공고번호', '참조번호', '공고명', '공고기관', '수요기관', '공고담당자', '집행관', '실제개찰일시', '복수예비가 및\n예정가격', '적격심사결과', '규격제안서 평가결과\n조회', '동일가격추첨결과', '유의사항']
    sleep(2)
    table = []
    table.append(driver.find_element(By.XPATH, '/html/body/div/div[2]/form[1]/div[2]/table'))
    tb2info = tools.adadvanced_table_info_read(table, bid_res_keys)

    # 테이블 정보 출력
    print(bid_res_keys)
    for i in range(len(tb2info[bid_res_keys[0]])):
        for key in bid_res_keys:
            if key != '유의사항':
                print(tb2info[key][i], end=' ')
        print()

    # 3.2 csv write
    tools.insert_value(tb2info, '입찰결과', pri_value)



def open_bid_rank_crawling(driver, pri_value): # 개찰결과순위 테이블 크롤링 함수
    # 1. 개찰순위 테이블 키 값 리스트 정의
    open_bid_keys = ['순위', '사업자등록번호', '업체명', '대표자', '투찰금액', '투찰률(%)', '추첨번호', '투찰일시', '비고']
    table = []
    table.append(driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/table'))
    tb1info = tools.adadvanced_table_info_read(table, open_bid_keys)

    # 테이블 정보 출력
    print(open_bid_keys)
    for i in range(len(tb1info[open_bid_keys[0]])):
        for key in open_bid_keys:
            print(tb1info[key][i], end=' ')
        print()
    tools.writeTb5(tb1info, 'bid_res')

    # 3. DB 저장
    # 3.1 tb 결측치 채우기
    for key in tb1info.keys():
        if key == '입찰공고번호':
            tb1info[key].clear()
            tb1info[key].append(pri_value)
        if tb1info[key] == []:
            tb1info[key].append('')

    # 3.2 csv write
    tools.insert_value(tb1info, '입찰결과', pri_value)


def Bid_Result_Detail_Page_Crawling(driver, pri_value):
    tstart = time.time()
    monitoring = Monitoring.monitoring()
    bid_res_crawling(driver, pri_value)
    open_bid_rank_crawling(driver, pri_value)
    monitoring.update('bid_res', time.time() - tstart, print_type='updated_element')

if __name__ == '__main__':
    Bid_Result_Detail_Page_Crawling()
