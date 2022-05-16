# 2. 개찰결과 크롤링 모듈
# cd C:\Program Files\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"
from collections import defaultdict

import os
print(os.getcwd())
# 셀레니움
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import pywinauto
from pywinauto import application
from pywinauto.application import Application

import pyperclip
import pyautogui

import time
from time import sleep

import readPreStandardDetail
import tools

# 개찰결과 데이터셋 수집 프로그램

# driver init
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
#
# driver = tools.driverInit(driver)

# 1. 검색 속성 설정 및 검색버튼 클릭

# 2. 리스트 순회
## 2.1. 리스트 정보 수집
## 2.1.1. 개찰 데이터 수집

#Move Next Page
def move_next_page():
    # 현재 페이지 출력
    # 마지막 페이지인지 확인 여부 출력
    pass

# 개찰결과 목록 리스트 정보 수집
def ListCrawling():
    readstart = time.time()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득

    driver = tools.driverInit(driver)

    # start = time.time()  # 시작 시간 저장
    #
    tb1_keys = ['업무','입찰공고번호','제입찰번호','공고명','수요기관','개찰일시','참가수','낙찰예정자','투찰금액/투찰금리','투찰률(%)','진행상황']
    tb1info = tools.initListDict(tb1_keys)

    table = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table')
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(11):
            body=value.find_elements(By.TAG_NAME,"td")[j]
            tb1info[tb1_keys[j]].append(body.text)

    #print(tb1info.items())
    list_len = len(tb1info['업무'])
    print("list",list_len, '읽어들인 시간 :', time.time() - readstart)  # 현재시각 - 시작시간 = 실행 시간
    u_len = 0 # 유찰 개수
    nu_len = 0 # 개찰완료, 재입찰 개수

    print(len(tb1info['업무']))

    # 목록 순환 소스
    for i in range(list_len):
        driver = tools.driverInit(driver)

        # print('키 값', tb1info[tb1_keys[-1]][i])
        if tb1info[tb1_keys[-1]][i] == '유찰': # 진행상황 == 유찰
            print('skip 유찰')
            u_len += 1
            continue
        # 진행상황 == '개찰완료' or '재입찰'
        else:
            nu_len += 1
            driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/table/tbody/tr['+str(i+1)+']/td[11]/div/a').click() # 해당 행이 개찰완료이면 개찰완료 버튼 클릭
            sleep(2) # 속도 수정
            # 개찰완료 페이지
            # 1. 입찰결과
            bid_res_crawling()
            # 2. 개찰순위
            open_bid_rank_crawling()
            # 3. 공고 상세
            sleep(1) # 이부분 속도 수정
            driver.back()
            sleep(1)
    print('페이지 순회 완료')
    print('해당 페이지 리스트 개수', list_len, '중 유찰 개수', u_len, '개찰완료or재입찰 개수', nu_len, '입니다')
    pass

# 입찰결과 목록 정보 수집
def ResultCrawling():
    readstart = time.time()
    # driver init 나중에 전역변수로 통일하는 작업 필요할 듯... 개발중에는 디버그 편한대로
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    # 1. 입찰결과 정보 수집

    # 2. 개찰순위 정보 수집


    pass
# bid : 입찰, open_bid : 개찰, announcement : 공고

# 물품개찰결과상세조회 페이지
def bid_res_crawling(): # 입찰결과 테이블 크롤링 함수
    # 1. 입찰결과 테이블 키 값 리스트 정의
    bid_res_keys = ['입찰공고번호', '참조번호', '공고명', '공고기관', '수요기관', '공고담당자', '집행관', '실제개찰일시', '복수예비가 및\n예정가격', '적격심사결과', '유의사항']

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    table = driver.find_element(By.XPATH, '/html/body/div/div[2]/form[1]/div[2]/table')
    tbody = table.find_element(By.TAG_NAME, "tbody")
    tb2info = tools.initListDict(bid_res_keys)
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        th_list = []
        for th in tr.find_elements(By.TAG_NAME, "th"):
            print(th.get_attribute("innerText"))
            th_list.append(th.get_attribute("innerText"))
        td_list = []
        for td in tr.find_elements(By.TAG_NAME, "td"):
            print(td.get_attribute("innerText"))
            td_list.append(td.get_attribute("innerText"))

        for i in range(len(th_list)):
            tb2info[th_list[i]].append(td_list[i])
    # print(tb2info)

    # 테이블 정보 출력
    print(bid_res_keys)
    for i in range(len(tb2info[bid_res_keys[0]])):
        for key in bid_res_keys:
            if key != '유의사항':
                print(tb2info[key][i], end=' ')
        print()
    pass

def open_bid_rank_crawling(): # 개찰결과순위 테이블 크롤링 함수
    # 1. 개찰순위 테이블 키 값 리스트 정의
    open_bid_keys = ['순위', '사업자등록번호', '업체명', '대표자', '투찰금액', '투찰률(%)', '추첨번호', '투찰일시', '비고']

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

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


announcement_common_keys = ['공고종류', '게시일시', '입찰공고번호', '참조번호', '공고명', '공고기관', '수요기관', '공고담당자', '집행관','검사','검수','입찰방식','낙찰방법','계약방법'
                                ,'국제입찰구분','재입찰','채권자명','발주계획통합번호','사전규격등록번호','사전규격 미공개사유','국내/국제 입찰사유','입찰자격','관련공고']

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[5]/table' ,announcement_common_keys, debug_mode = True)
    print(tb_info.items())

    pass
def bid_info_crawling(): # 3. 예정가격 결정 및 입찰금액 정보
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    bid_info_keys = ['예가방법', '추첨번호공개여부', '사업금액\n(추정가격 + 부가세)', '추정가격', '배정예산']

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[9]/table', bid_info_keys,
                                    debug_mode=True)
    print(tb_info.items())
    pass
def xnkfwpgks(): # 3. 투찰제한 - 일반
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    bid_info_keys = ['지역제한', '업종제한', '물품분류제한여부', '물품등록구분', '공동수급체 구성원 지역제한적용여부']

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[11]/table', bid_info_keys,
                                    debug_mode=True)
    print(tb_info.items())
    pass

def bid_cost_infomation(): # 2. 입찰진행 및 진행정보
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    bid_info_keys = ['입찰개시일시', '입찰마감일시', '개찰(입찰)일시', '물품등록구분', '개찰(입찰)일시','개찰장소','입찰참가자격등록\n마감일시','보증서접수마감일시','실적심사신청서','실적심사신청서\n신청기한','공동수급협정서\n접수여부','동가입찰 낙찰자\n자동추첨프로그램','공동수급협정서\n마감일시','연구개발물품여부']

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[7]/table', bid_info_keys,
                                    debug_mode=True)
    print(tb_info.items())
    pass

def announce_doc():
    file_name = 'hwp' # 수정
    findWord = ['±', '낙찰하한율']
    file_path = os.path.join(download_path, file_name)
    range, min_value = readHWP.announcement_doc_crawling(file_path, findWord) # 범위, 낙찰하한율 반환

    return range, min_value

# 1. 공고 일반
announcement_common_keys = ['공고종류', '게시일시', '입찰공고번호', '참조번호', '공고명', '공고기관', '수요기관', '공고담당자', '집행관','검사','검수','입찰방식','낙찰방법','계약방법','국제입찰구분','재입찰','채권자명','발주계획통합번호','사전규격등록번호','사전규격 미공개사유','국내/국제 입찰사유','입찰자격','관련공고']
bid_info_keys = ['예가방법', '추첨번호공개여부', '사업금액\n(추정가격 + 부가세)', '추정가격', '배정예산']
rkdydrmador_keys = ['입찰분류', '가용금액']
rlchrmador_keys = ['분류', '기초금액','비고','상세보기']
rnaoeotkd1_keys = ['분류', '수요기관', '세부품명', '납품장소'] # table type3 :  속성이 나눠져있음
rnaoeotkd2_keys = ['수량','단위','추정 단가(원)','세부품명번호','규격','납품 기한(일수)','인도 조건']
dlqckfwlsgod_keys = ['입찰공고번호', '재입찰번호','공고명','개찰일시','진행현황']

def announcement_detail_crawling(): # 물품 입찰 공고 상세 페이지 크롤링 함수, 함수 이름 바꿔야댐
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    # 수집 항목 : 사업금액, 배정예산, 지역제한, 기초금액, 낙찰하한율, 범위
    # 페이지 수집 항목
    # 사업금액 : 물품입찰공고상세페이지 참조
    # 1. 공고 일반
    announcement_common_crawling()

    # 2.입찰진행 및 진행 정보
    bid_info_crawling()
    # 3. 예정가격 결정
    bid_cost_infomation()

    # 3. 투찰제한 - 일반
    xnkfwpgks()

    # 4. 가용금액 공개
    rkdydrmador()

    # 5. 기초금액 공개
    rlchrmador()

    # 6. 구매대상물품
    rnaoeotkd()

    # 8. 입찰진행현황
    dlqckfwlsgod()

    # 7. 첨부 파일
    # 공고문 수집 항목
    # 낙찰하한율 : 공고문에서 낙찰하한율 검색
    # 범위 : 공고문에서 +- 검색

    # f. 입찰공고문 열람 확인버튼 클릭

    # f. 공고문 다운로드

    # ff. 공고문 읽기
    # announce_doc()

    pass

def announcement_common_crawling(): # 1. 공고 일반
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[5]/table' ,announcement_common_keys, debug_mode = True)
    print(tb_info.items())

    pass
def bid_info_crawling(): # 3. 예정가격 결정 및 입찰금액 정보
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    bid_info_keys = ['예가방법', '추첨번호공개여부', '사업금액\n(추정가격 + 부가세)', '추정가격', '배정예산']

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[9]/table', bid_info_keys,
                                    debug_mode=True)
    print(tb_info.items())
    pass
def xnkfwpgks(): # 3. 투찰제한 - 일반
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    bid_info_keys = ['지역제한', '업종제한', '물품분류제한여부', '물품등록구분', '공동수급체 구성원 지역제한적용여부']

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[11]/table', bid_info_keys,
                                    debug_mode=True)
    print(tb_info.items())
    pass

def bid_cost_infomation(): # 2. 입찰진행 및 진행정보
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    bid_info_keys = ['입찰개시일시', '입찰마감일시', '개찰(입찰)일시', '물품등록구분', '개찰(입찰)일시','개찰장소','입찰참가자격등록\n마감일시','보증서접수마감일시','실적심사신청서','실적심사신청서\n신청기한','공동수급협정서\n접수여부','동가입찰 낙찰자\n자동추첨프로그램','공동수급협정서\n마감일시','연구개발물품여부']

    tb_info = tools.table_info_read(driver, '/html/body/div[2]/div[2]/div[7]/table', bid_info_keys,
                                    debug_mode=True)
    print(tb_info.items())
    pass

def announce_doc():
    file_name = 'hwp' # 수정
    findWord = ['±', '낙찰하한율']
    file_path = os.path.join(download_path, file_name)
    range, min_value = readHWP.announcement_doc_crawling(file_path, findWord) # 범위, 낙찰하한율 반환

    return range, min_value

# 4. 가용금액 공개
def rkdydrmador():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    rkdydrmador_keys = ['입찰분류', '가용금액']
    tb1info = tools.initListDict(rkdydrmador_keys)

    table = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[13]/table') # 리스트 타입의 테이블을 읽어들임
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(len(rkdydrmador_keys)):
            # 데이터가 없을 경우
            if value.find_element(By.TAG_NAME,"td").text == '공개된 정보가 없습니다.':
                tb1info[rkdydrmador_keys[j]].append('')
            # 데이터가 있을 경우
            else:
                body=value.find_elements(By.TAG_NAME,"td")[j]
                # print(body.text) # debug
                tb1info[rkdydrmador_keys[j]].append(body.text)

    print(tb1info.items())
    pass

# 5. 기초금액 공개
def rlchrmador():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    rlchrmador_keys = ['분류', '기초금액','비고','상세보기']
    tb1info = tools.initListDict(rlchrmador_keys)

    table = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[16]/table') # 리스트 타입의 테이블을 읽어들임
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(len(rlchrmador_keys)):
            # 데이터가 없을 경우
            if value.find_element(By.TAG_NAME,"td").text == '공개된 정보가 없습니다.':
                tb1info[rkdydrmador_keys[j]].append('')
            # 데이터가 있을 경우
            else:
                body=value.find_elements(By.TAG_NAME,"td")[j]
                # print(body.text) # debug
                tb1info[rlchrmador_keys[j]].append(body.text)

    print(tb1info.items())

    pass

# 6. 구매대상물품
def rnaoeotkd():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    rnaoeotkd1_keys = ['분류', '수요기관', '세부품명', '납품장소'] # table type3 :  속성이 나눠져있음
    rnaoeotkd2_keys = ['수량','단위','추정 단가(원)','세부품명번호','규격','납품 기한(일수)','인도 조건']


    tb1info = tools.initListDict(rnaoeotkd1_keys+rnaoeotkd2_keys)

    table = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[19]/table') # 리스트 타입의 테이블을 읽어들임
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        if i == 0:
            continue
        elif i == 1:
            keys = rnaoeotkd1_keys
        else:
            keys = rnaoeotkd2_keys
        for j in range(len(keys)):
            # 데이터가 없을 경우
            if value.find_element(By.TAG_NAME,"td").text == '공개된 정보가 없습니다.':
                tb1info[keys[j]].append('')
            # 데이터가 있을 경우
            else:
                body=value.find_elements(By.TAG_NAME,"td")[j]
                # print(body.text) # debug
                tb1info[keys[j]].append(body.text)

    print(tb1info.items())


    pass

# 8. 입찰진행현황
def dlqckfwlsgod():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options) # 위 cmd 명령어로 실행된 크롬 제어 권한을 획득
    driver = tools.driverInit(driver)

    dlqckfwlsgod_keys = ['입찰공고번호', '재입찰번호','공고명','개찰일시','진행현황']
    tb1info = tools.initListDict(dlqckfwlsgod_keys)

    table = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[23]/table') # 리스트 타입의 테이블을 읽어들임
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows):
        for j in range(len(dlqckfwlsgod_keys)):
            # 데이터가 없을 경우
            if value.find_element(By.TAG_NAME,"td").text == '공개된 정보가 없습니다.':
                tb1info[dlqckfwlsgod_keys[j]].append('')
            # 데이터가 있을 경우
            else:
                body=value.find_elements(By.TAG_NAME,"td")[j]
                # print(body.text) # debug
                tb1info[dlqckfwlsgod_keys[j]].append(body.text)

    print(tb1info.items())

    pass

if __name__ == '__main__':
    tstart = time.time()
    announcement_detail_crawling()
    # ListCrawling()
    # ResultCrawling()
    # bid_res_crawling()
    # open_bid_rank_crawling()



    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간