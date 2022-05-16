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

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
driver = tools.driverInit(driver)

## table elements
table_element_list = []
## table names
table_names = ['공고일반', '입찰진행 및 진행정보', '예정가격 결정 및 입찰금액 정보', '투찰제한 - 일반', '가용금액공개', '기초금액 공개', '구매대상물품', '입찰진행현황']

## info_tables : table dic 'table_name', table_keys'
info_tables = tools.initListDict(table_names)
info_tables['공고일반'].append(['공고종류', '게시일시', '입찰공고번호', '참조번호', '공고명', '공고기관', '수요기관', '공고담당자', '집행관','검사','검수','입찰방식','낙찰방법','계약방법','국제입찰구분','재입찰','채권자명','발주계획통합번호','사전규격등록번호','사전규격 미공개사유','국내/국제 입찰사유','WTO수의계약사유','입찰자격','관련공고'])
info_tables['입찰진행 및 진행정보'].append(['입찰개시일시', '입찰마감일시', '개찰(입찰)일시', '물품등록구분', '개찰(입찰)일시','개찰장소','입찰참가자격등록\n마감일시','보증서접수마감일시','실적심사신청서','실적심사신청서\n신청기한','공동수급협정서\n접수여부','동가입찰 낙찰자\n자동추첨프로그램','공동수급협정서\n마감일시','연구개발물품여부'])
info_tables['예정가격 결정 및 입찰금액 정보'].append(['예가방법', '추첨번호공개여부', '사업금액\n(추정가격 + 부가세)', '추정가격', '배정예산'])
info_tables['투찰제한 - 일반'].append(['지역제한', '참가가능지역', '지사투찰허용여부', '업종제한', '물품분류제한여부', '물품등록구분', '공동수급체 구성원 지역제한적용여부'])
info_tables['가용금액공개'].append(['입찰분류', '가용금액'])
info_tables['기초금액 공개'].append(['분류', '기초금액','비고','상세보기'])
info_tables['구매대상물품'].append(['분류', '수요기관', '세부품명', '납품장소'])
info_tables['구매대상물품'].append(['수량','단위','추정 단가(원)','세부품명번호','규격','납품 기한(일수)','인도 조건'])
info_tables['입찰진행현황'].append(['입찰공고번호', '재입찰번호','공고명','개찰일시','진행현황'])

def announcement_detail_crawling(): # 물품 입찰 공고 상세 페이지 크롤링 함수, 함수 이름 바꿔야댐
    # 1. 물품 입찰공고 상세 페이지 table 정보 수집
    tb1_info = tools.advanced_table_info_read(table_element_list[0], info_tables['공고일반'][0]) # 1. 공고 일반
    tb2_info = tools.advanced_table_info_read(table_element_list[1], info_tables['입찰진행 및 진행정보'][0]) # 2. 입찰집행 및 진행정보
    tb3_info = tools.advanced_table_info_read(table_element_list[2], info_tables['예정가격 결정 및 입찰금액 정보'][0]) # 3. 예정가격 결정 및 입찰금액 정보
    tb4_info = tools.advanced_table_info_read(table_element_list[3], info_tables['투찰제한 - 일반'][0])  # 4. 투찰제한 - 일반
    tb5_info = tools.advanced_table1_info_read(table_element_list[4], info_tables['가용금액공개'][0])  # 5. 가용금액 공개
    tb6_info = tools.advanced_table1_info_read(table_element_list[5], info_tables['기초금액 공개'][0]) # 6. 기초금액 공개
    tb8_info = tools.advanced_table1_info_read(table_element_list[7], info_tables['입찰진행현황'][0]) # 7.입찰진행현황

    # 2. 첨부파일 규격서 정보 수집
    # 2.1. 공고서 다운로드
    # 2.2. 공고서 정보 수집


# def rnaoeotkd(): # # 7. 구매대상물품
#     keys1 = rnaoeotkd1_keys.copy()
#     keys2 = rnaoeotkd2_keys.copy()
#     tb1info = tools.initListDict(keys1 + keys2)
#
#     table = table_element_list[6] # 리스트 타입의 테이블을 읽어들임
#     tbody = table.find_element(By.TAG_NAME, "tbody")
#     rows = tbody.find_elements(By.TAG_NAME, "tr")
#     for i, value in enumerate(rows):
#         if i == 0:
#             continue
#         elif i == 1:
#             keys = rnaoeotkd1_keys
#         else:
#             keys = rnaoeotkd2_keys
#         for j in range(len(keys)):
#             # 데이터가 없을 경우
#             if value.find_element(By.TAG_NAME,"td").text == '공개된 정보가 없습니다.':
#                 tb1info[keys[j]].append('')
#             # 데이터가 있을 경우
#             else:
#                 body=value.find_elements(By.TAG_NAME,"td")[j]
#                 tb1info[keys[j]].append(body.text)

def announce_doc():
    file_name = 'hwp' # 수정
    findWord = ['±', '낙찰하한율']
    file_path = os.path.join(download_path, file_name)
    range, min_value = readHWP.announcement_doc_crawling(file_path, findWord) # 범위, 낙찰하한율 반환

    return range, min_value


def search_table_xpath(): # table elements 탐색
    tables_xpath = driver.find_elements(By.TAG_NAME, 'table')  # 리스트 타입의 테이블을 읽어들임
    for table_names in info_tables.keys():
        if table_names == '구매대상물품':
            table_keys = info_tables[table_names][0].copy() + info_tables[table_names][1].copy()
        else:
            table_keys = info_tables[table_names][0].copy()

        for table_xpath in tables_xpath:
            s_b = False
            for key in table_keys:
                if table_xpath.text.find(key) != -1:
                    table_element_list.append(table_xpath)
                    s_b = True
                    tables_xpath.remove(table_xpath)
                    break
            if s_b == True:
                break

if __name__ == '__main__':
    tstart = time.time()
    search_table_xpath()
    announcement_detail_crawling()

    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간