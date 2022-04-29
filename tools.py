import openpyxl as xl
import pandas as pd

def writeTb1(tbinfo): # 크롤링 데이터 메타정보 저장함수
    pass

def writeTb2(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb2.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb3(tbinfo): # 크롤링 데이터 메타정보 저장함수
    db = pd.DataFrame(tbinfo, columns=tbinfo.keys())
    db.to_csv('tb3.csv', mode='a', header=False, index=True, encoding='utf-8-sig')

def writeTb4(tbinfo): # 크롤링 데이터 메타정보 저장함수
    pass

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
