import openpyxl as xl

def writeMetainfo(tbinfo): # 크롤링 데이터 메타정보 저장함수
    pass


wb = xl.load_workbook('크롤링.xlsx')
for sheet_nm in wb.sheetnames:
    print('*' * 100)
    print('시트명:', sheet_nm)
    sheet = wb[sheet_nm]
    for row_data in sheet.iter_rows(min_row=1): # min_row는 시작 행을 지정 for cell in row_data: print('[', cell.value, ']') print('=' * 100) wb.close()
        for cell in row_data:
            print('[', cell.value, ']')
        print('=' * 100)

wb.close()
