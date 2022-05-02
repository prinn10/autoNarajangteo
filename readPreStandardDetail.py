# 셀레니움
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from collections import defaultdict

import time
from time import sleep
import os

import readHWP
import tools

tb2_keys = ['참조번호', '사전규격등록번호', '품명','품명(사업명)','사업명', '배정예산액', '관련 사전규격번호', '공개일시', '의견등록마감일시', '공고기관', '수요기관', 'SW사업대상여부', '납품(완수)기한\n(납품일수)', '규격서 파일', '적합성여부']
tb3_keys = ['사전규격등록번호', '파일명', '0036', '8111179901', '4321150102']
def readPage(driver):
    driver = tools.driverInit(driver)
    download_path = 'C:\\Users\\정희운\\Downloads'
    # 1. 테이블 정보 읽어오기
    table = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/table')
    tbody = table.find_element_by_tag_name("tbody")
    tb2info = tools.initListDict(tb2_keys)
    tb3info = tools.initListDict(tb3_keys)
    for tr in tbody.find_elements_by_tag_name("tr"):
        th_list = []
        for th in tr.find_elements_by_tag_name("th"):
            print(th.get_attribute("innerText"))
            th_list.append(th.get_attribute("innerText"))
        td_list = []
        for td in tr.find_elements_by_tag_name("td"):
            print(td.get_attribute("innerText"))
            td_list.append(td.get_attribute("innerText"))

        for i in range(len(th_list)):
            tb2info[th_list[i]].append(td_list[i])

    item_name_list = ['관련 사전규격번호', '품명', '품명(사업명)', '사업명']
    for item_name in item_name_list:
        if tb2info.get(item_name) == []:
            tb2info[item_name].append('')

    # for key, val in tb2info.items():
    #     print('k' , key, 'v', val)

    # 2. 첨부파일 다운로드 및 영업 적합성 여부 판단
    ## 2.1. 첨부파일 다운로드
    downloadCheck = False
    ### 2.1.1. 규격서 파일 다운로드
    file_list = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/table/tbody/tr[8]/td/div/a')
    if len(file_list) != 0:
        print('파일 개수', len(file_list))
        downloadCheck = True
        for file in file_list:
            print('파일 다운로드')
            file.click()
            sleep(1)
    else:
        print('규격서 파일 존재하지 않음')

    ### 2.1.2. [첨부파일 (e-발주시스템)] 다운로드
    try:
        driver.switch_to.frame(driver.find_element_by_id('eRfpReqIframe'))
        driver.find_element_by_class_name('file_name').click()
        print('[첨부파일 (e-발주시스템)] 다운로드 완료')
        downloadCheck = True
        driver = tools.driverInit(driver)
        sleep(1)
    except NoSuchElementException:
        driver = tools.driverInit(driver)
        print('[첨부파일 (e-발주시스템)] 존재하지 않음')

    ## 2.2 영업 적합성 여부 판단
    start = time.time()  # 시작 시간 저장

    okng = False
    if downloadCheck == True:
        tools.waitFileDownload(download_path)

        file_list = os.listdir(download_path)
        print(file_list)
        keyword_list = ['0036', '8111179901', '4321150102']
        for j, file in enumerate(file_list):
            tb3info['사전규격등록번호'].append(tb2info['사전규격등록번호'][0])
            tb3info['파일명'].append(str(file))
            if file.find('hwp') != -1:
                res_list = readHWP.advanced_open_and_findtext(os.path.join(download_path, file), keyword_list)
                for res, keyword in zip(res_list, keyword_list):
                    if res == True:
                        print(file, keyword,'존재확인')
                        tb3info[keyword].append('True')
                        okng = True
                    else:
                        print(file, keyword, '존재하지않습니다')
                        tb3info[keyword].append('False')
            else:
                for keyword in keyword_list:
                    tb3info[keyword].append('None')
            os.remove(os.path.join(download_path, file)) # 확인 후 해당 파일 삭제
    else:
        print('다로드된 파일이 없음')

    print("적합성 여부 판단 시간 :", time.time() - start)

    if okng == True:
        tb2info['적합성여부'] = 'True'
    else:
        tb2info['적합성여부'] = 'False'

    # print(tb2info.keys())
    # print(tb3info.keys())

    return tb2info, tb3info, okng


# 사전규격 상세 (물품) 페이지 읽는 함수
# 해당 페이지를 읽어들여서 다음의 값을 반환한다.
# 1. excel 기입에 필요한 테이블 정보를 담은 dictionary 인스턴스
# 2. 첨부파일을 읽고 해당 페이지의 영업 적합 여부 값을 저장한 boolean 인스턴스
