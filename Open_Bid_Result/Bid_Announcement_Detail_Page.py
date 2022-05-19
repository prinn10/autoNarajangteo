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

def Init():
    # chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    # driver = tools.driverInit(driver)

    ## table names
    table_names = ['공고일반', '입찰집행 및 진행 정보', '예정가격 결정 및 입찰금액 정보', '가용금액공개', '기초금액 공개', '첨부 파일', '입찰진행현황']

    ## table elements
    table_element_list = tools.initListDict(table_names)

    ## info_tables : table dic 'table_name', table_keys'
    info_tables = tools.initListDict(table_names)
    info_tables['공고일반'].append(['공고종류', '게시일시', '입찰공고번호', '참조번호', '공고명', '공고기관', '수요기관', '공고담당자', '집행관','검사','검수','입찰방식','낙찰방법','계약방법','국제입찰구분','재입찰','채권자명','발주계획통합번호','사전규격등록번호','사전규격 미공개사유','국내/국제 입찰사유','WTO수의계약사유','입찰자격','관련공고'])
    info_tables['입찰집행 및 진행 정보'].append(['입찰개시일시', '입찰마감일시', '개찰(입찰)일시', '물품등록구분', '개찰(입찰)일시','개찰장소','입찰참가자격등록\n마감일시','보증서접수마감일시','실적심사신청서','실적심사신청서\n신청기한','공동수급협정서\n접수여부','동가입찰 낙찰자\n자동추첨프로그램','공동수급협정서\n마감일시','연구개발물품여부'])
    info_tables['예정가격 결정 및 입찰금액 정보'].append(['예가방법', '추첨번호공개여부', '사업금액\n(추정가격 + 부가세)', '추정가격', '배정예산'])
    # info_tables['투찰제한 - 일반'].append(['지역제한', '참가가능지역', '지사투찰허용여부', '업종제한','업종사항제한', '물품분류제한여부', '물품등록구분', '공동수급체 구성원 지역제한적용여부'])
    info_tables['가용금액공개'].append(['입찰분류', '가용금액'])
    info_tables['기초금액 공개'].append(['분류', '기초금액','비고','상세보기'])
    # info_tables['구매대상물품'].append(['분류', '수요기관', '세부품명', '납품장소'])
    # info_tables['구매대상물품'].append(['수량','단위','추정 단가(원)','세부품명번호','규격','납품 기한(일수)','인도 조건'])
    info_tables['첨부 파일'].append(['No.','문서구분','파일명'])
    info_tables['입찰진행현황'].append(['입찰공고번호', '재입찰번호','공고명','개찰일시','진행현황'])

    return table_names, table_element_list, info_tables

def announcement_detail_crawling(table_names, table_element_list, info_tables): # 물품 입찰 공고 상세 페이지 크롤링 함수, 함수 이름 바꿔야댐
    # 1. 물품 입찰공고 상세 페이지 table 정보 수집
    tb_info = []
    for i, table_name in enumerate(table_names):
        if table_name == '공고일반' or table_name == '입찰집행 및 진행 정보' or table_name == '예정가격 결정 및 입찰금액 정보':# table type 1(th td th td)
            tb_info.append(tools.advanced_table_info_read(table_element_list[table_name][0], info_tables[table_name][0]))
        elif table_name == '가용금액공개' or table_name == '기초금액 공개' or table_name == '첨부 파일' or table_name == '입찰진행현황': # table type 2 (list table)
            tb_info.append(tools.advanced_table1_info_read(table_element_list[table_name][0], info_tables[table_name][0]))
        print('table_name : ', table_name)
        print(tb_info[i])

    # 2. 첨부파일 규격서 정보 수집
    # 2.1. 공고서 탐색 및 다운로드
    try:
        i = tb_info[5]['문서구분'].index('공고서')
        tbody = table_element_list['첨부 파일'][0].find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        rows[i].find_elements(By.TAG_NAME,"td")[2].find_element(By.TAG_NAME,"a").click()

        # 2.2. 공고서 정보 수집
        download_path = 'C:\\Users\\정희운\\Downloads'
        tools.waitFileDownload(download_path)
        sleep(2)
        file_name = os.listdir(download_path)
        findWord = ['±', '낙찰하한율', '예정가격']
        range, min_value = readHWP.announcement_doc_crawling(os.path.join(download_path, file_name[0]), findWord) # 범위, 낙찰하한율 반환
        os.remove(os.path.join(download_path, file_name[0]))  # 확인 후 해당 파일 삭제
        tb_info.append({'±': [range], '낙찰하한율': [min_value]})
        print(tb_info[7])
    except:
        print('공고서 없음')

    # 3. DB 저장
    # 3.1 tb 결측치 채우기
    for tb in tb_info:
        for key in tb.keys():
            if tb[key] == []:
                tb[key].append('')

    # 3.2 csv write
    for i, tb in enumerate(tb_info):
        tools.writeTb5(tb, 'bid_detail'+str(i+1))


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

# def announce_doc():
#     file_name = 'hwp' # 수정
#     findWord = ['±', '낙찰하한율']
#     file_path = os.path.join(download_path, file_name)
#     range, min_value = readHWP.announcement_doc_crawling(file_path, findWord) # 범위, 낙찰하한율 반환
#
#     return range, min_value
#

def search_table_xpath(table_element_list, info_tables): # table elements 탐색
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)  # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    tables_xpath = driver.find_elements(By.TAG_NAME, 'table')  # 리스트 타입의 테이블을 읽어들임
    for table_names in info_tables.keys():
        if table_names == '구매대상물품':
            table_keys = info_tables[table_names][0].copy() + info_tables[table_names][1].copy()
        else:
            table_keys = info_tables[table_names][0].copy()

        for table_xpath in tables_xpath:
            if table_xpath.get_attribute("summary").find(table_names[0:3]) != -1:
                table_element_list[table_names].append(table_xpath)


    for key, val in table_element_list.items():
        print('---------------------',key)
        print(val)

    return table_element_list



def Bid_Announcement_Detail_Page_Crawling():
    table_names, table_element_list, info_tables = Init()
    table_element_list = search_table_xpath(table_element_list, info_tables)
    announcement_detail_crawling(table_names, table_element_list, info_tables)

if __name__ == '__main__':
    tstart = time.time()
    Bid_Announcement_Detail_Page_Crawling()
    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간