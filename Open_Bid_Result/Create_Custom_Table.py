import tools
import os
import csv
# 학습에 필요한 변수만 수집하여 저장하는 기능을 제공

# 페이지 정보
# 1. 개찰결과 목록
# 2. 물품 개찰결과 상세조회
# 3. 물품 입찰공고 상세
# 4. 예비가격 산정결과
# 페이지 별 테이블 정보
# 1.1.개찰결과 목록
# 2.1 입찰결과
# 2.2 개찰순위
# 3.1 공고일반
# 3.2 입찰집행 및 진행 정보
# 3.3 예정가격 결정 및 입찰금액 정보
# 3.4 투찰제한 - 일반
# 3.5 가용금액공개
# 3.6 기초금액 공개
# 3.7 구매대상물품
# 3.8 첨부 파일
# 3.9 입찰진행현황
# 3.10 공고문
# 4.1 입찰공고정보
# 4.2 예비가격 정보제공
# 4.3 기초금액 정보

def Init():
    dataset_path = 'C:\\pycharm\\source\\autoNarajangteo\\Open_Bid_Result\\Dataset'

    keys = ['입찰공고번호','기초금액','예정가격', '예가범위', '참여업체수', '낙찰하한율', '기초금액기준 상위개수', '투찰금액(원)', '투찰률(%)']
    file_names = ['bid_detail1.csv', '예비가격산정결과2.csv', '예비가격산정결과2.csv', '예비가격산정결과1.csv', 'lis_cra.csv', 'bid_detail8.csv', '예비가격산정결과1.csv','개찰순위','개찰순위']
    read_lines = [3, 2, 1, 8, 7, 2, 9, 4, 5]
    tb_info = tools.initListDict(keys)


    for key, file_name, read_line in zip(keys, file_names, read_lines):
        if key == '입찰공고번호':
            f = open(os.path.join(dataset_path,file_name), 'r', encoding='UTF8')
            rdr = csv.reader(f)
            for line in rdr:
                tb_info[key].append(line[read_line])
            f.close()

    for pri_value in tb_info['입찰공고번호']:
        for key, file_name, read_line in zip(keys, file_names, read_lines):
            if key != '입찰공고번호':
                f = open(os.path.join(dataset_path,file_name), 'r', encoding='UTF8')
                rdr = csv.reader(f)
                for line in rdr:
                    if pri_value in line:
                        tb_info[key].append(line[read_line])
                        break
                f.close()


    tb_info = tools.insert_value(tb_info, 'dataset', pri_value=None, save_path=dataset_path)
    tb_info = del_element(tb_info)
    tb_info = extract_range(tb_info)
    tb_info = rowDel(tb_info)
    tb_info = overlap(tb_info)
    tb_info = plusMinus(tb_info)
    tb_info = commaDel(tb_info)
    tb_info = tools.insert_value(tb_info, 'dataset2', pri_value=None, save_path=dataset_path)

def del_element(tb_info): #결측치 제거
    i=0
    lenth = len(tb_info['입찰공고번호'])
    while i < lenth:
        print(i, lenth)
        for key in tb_info.keys():
            if tb_info[key][i] == '':
                for key in tb_info.keys():
                    del tb_info[key][i]
                i -= 1
                lenth = len(tb_info['입찰공고번호'])
                break
        i += 1
    return tb_info

def extract_range(tb_info): # 예가범위 전처리
    tb_info['예가범위1'] = []
    tb_info['예가범위2'] = []
    for i in range(len(tb_info['입찰공고번호'])):
            num_list = tools.extract_number(tb_info['예가범위'][i])
            tb_info['예가범위1'].append(num_list[0])
            tb_info['예가범위2'].append(num_list[1])
    tb_info.pop('예가범위')
    return tb_info

def unique_row(tb_info): # 중복행 제거
    pass

def Custom_Table():
    # tstart = time.time()
    Init()
     #print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간

def rowDel(tb_info):
    i = 0
    delCnt = 0
    while True:
        for key in tb_info.keys():
            if tb_info[key][i] == '':
                for keyy in tb_info.keys():
                    del tb_info[keyy][i]
                i -= 1
                delCnt += 1
                break
        i += 1
        if i >= len(tb_info['입찰공고번호']):
            break
    return tb_info


def overlap(tb_info):
    i = 0
    ovlCnt = 0
    while True:
        j = i + 1
        while True:
            if tb_info['입찰공고번호'][i] == tb_info['입찰공고번호'][j]:
                ovlCnt += 1
                print(tb_info['입찰공고번호'][i],tb_info['입찰공고번호'][j])
                for key in tb_info.keys():
                    del tb_info['입찰공고번호'][j]
                j -= 1
            j += 1
            if j > len(tb_info['입찰공고번호']) - 1:
                break
        i += 1
        if i > len(tb_info['입찰공고번호'])-2:
            break
    print("overlaps = ", ovlCnt)
    return tb_info


def plusMinus(tb_info):
    for i in range(len(tb_info['예가범위'])):
        # print(tb_info['예가범위'][i])
        if tb_info['예가범위'][i].find('3') != -1:
            tb_info['예가범위'][i] = '3'
        elif tb_info['예가범위'][i].find('2') != -1:
            tb_info['예가범위'][i] = '2'
        elif tb_info['예가범위'][i].find('1') != -1:
            tb_info['예가범위'][i] = '1'
        else:
            tb_info['예가범위'][i] = '0'
    return tb_info


def commaDel(tb_info):
    for i in range(len(tb_info['기초금액'])):
        tb_info['기초금액'][i] =  tb_info['기초금액'][i].replace(",", "")
    for i in range(len(tb_info['예정가격'])):
        tb_info['예정가격'][i] = tb_info['예정가격'][i].replace(",", "")
    return tb_info

if __name__ == '__main__':
    Custom_Table()