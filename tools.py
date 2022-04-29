import openpyxl as xl
import pandas as pd
from time import sleep
import os

def writeTb1(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb1.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb2(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb2.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb3(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb3.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb4(tbinfo): # 크롤링 데이터 메타정보 저장함수
    pass

def initListDict(keys):
    ListDict = {}
    for key in keys:
        ListDict[key] = []
    return ListDict

def waitFileDownload(download_path):
    while True:
        file_list = os.listdir(download_path)
        all_check = False
        for file in file_list:
            if str(file).find('crdownload') != -1:
                sleep(0.3)
                print('다운로드 대기 중...')
                all_check = True
        if all_check == False:
            break



#
# wb = xl.load_workbook('크롤링.xlsx')
# for sheet_nm in wb.sheetnames:
#     print('*' * 100)
#     print('시트명:', sheet_nm)
#     sheet = wb[sheet_nm]
#     for row_data in sheet.iter_rows(min_row=1): # min_row는 시작 행을 지정 for cell in row_data: print('[', cell.value, ']') print('=' * 100) wb.close()
#         for cell in row_data:
#             print('[', cell.value, ']')
#         print('=' * 100)
#
# wb.close()
