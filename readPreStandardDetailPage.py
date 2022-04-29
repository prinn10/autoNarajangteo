from time import sleep
from selenium.common.exceptions import NoSuchElementException
import os
import readHWP

def readPage(driver):
    download_path = 'C:\\Users\\정희운\\Downloads'
    # 1. 테이블 정보 읽어오기
    table = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/table')
    tbody = table.find_element_by_tag_name("tbody")
    tbinfo = {}
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
            tbinfo[th_list[i]] = td_list[i]

    for key, val in tbinfo.items():
        print('k' , key, 'v', val)

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
            sleep(2)
    else:
        print('규격서 파일 존재하지 않음')

    ### 2.1.2. [첨부파일 (e-발주시스템)] 다운로드
    try:
        driver.switch_to.frame(driver.find_element_by_id('eRfpReqIframe'))
        driver.find_element_by_class_name('file_name').click()
        print('[첨부파일 (e-발주시스템)] 다운로드 완료')
        downloadCheck = True
        sleep(4)
    except NoSuchElementException:
        print('[첨부파일 (e-발주시스템)] 존재하지 않음')
        pass

    ## 2.2 영업 적합성 여부 판단
    okng = False
    if downloadCheck == True:
        file_list = os.listdir(download_path)
        print(file_list)
        keyword = ['0036', '8111179901', '4321150102']
        for file in file_list:
            for i in range(len(keyword)):
                if file.find('hwp') != -1:
                    res = readHWP.open_and_findtext(os.path.join(download_path, file), keyword[i])
                    if res == True:
                        print(file, keyword[i],'존재확인')
                        okng = True
                    else:
                        print(file, keyword[i], '존재하지않습니다')

        # for file in file_list:
        #     os.remove(os.path.join(download_path, file)) # 확인 후 해당 파일 삭제

    else:
        print('다로드된 파일이 없음')

    return tbinfo, okng


# 사전규격 상세 (물품) 페이지 읽는 함수
# 해당 페이지를 읽어들여서 다음의 값을 반환한다.
# 1. excel 기입에 필요한 테이블 정보를 담은 dictionary 인스턴스
# 2. 첨부파일을 읽고 해당 페이지의 영업 적합 여부 값을 저장한 boolean 인스턴스
