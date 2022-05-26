import tools
import os
import csv
# 학습에 필요한 변수만 수집하여 저장하는 기능을 제공

def Init():
    dataset_path = r"Dataset"

    keys = ['입찰공고번호','기초금액','예정가격','예가범위','참여업체수', '낙찰하한율', '기초금액기준 상위개수']
    file_names = ['bid_detail1.csv', '예비가격산정결과2.csv', '예비가격산정결과2.csv', '예비가격산정결과1.csv', 'lis_cra.csv', 'bid_detail8.csv', '예비가격산정결과1.csv']
    read_lines = [3, 2, 1, 8, 7, 2, 9]
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

    tb_info = rowDel(tb_info) #결측치 제거
    tb_info = unique_element(tb_info) #중복값 제거
    tb_info = extract_range(tb_info) # 예가범위 전처리

    # 투찰 요소 추가
    tb_info['투찰금액'] = []
    tb_info['투찰률'] = []
    for i in range(len(tb_info['입찰공고번호'])):
        a, b = open_bid_rank(tb_info['입찰공고번호'][i])
        tb_info['투찰금액'].append(a)
        tb_info['투찰률'].append(b)

    tb_info = rowDel(tb_info) #결측치 제거

    tb_info = cal_target(tb_info) # 목표 투찰률 항목 추가
    tb_info = commaDel(tb_info) # 금액속성 , 제거

    print(tb_info.keys())
    tb_info = tools.insert_value(tb_info, 'dataset_result', pri_value=None, save_path=dataset_path)
def cal_target(tb_info): # 목표 투찰률 계산
    tb_info['target rate'] = []
    for i in range(len(tb_info['입찰공고번호'])):
        a = float(tb_info['낙찰하한율'][i])
        b = float(tb_info['투찰률'][i])
        res = round((a+b)/2, 4)
        tb_info['target rate'].append(str(res))
    return tb_info
def open_bid_rank(bid_ann_num):
    f = open(os.path.join(r"Dataset",'개찰순위.csv'), 'r', encoding='UTF8')
    rdr = csv.reader(f)
    for line in rdr:
        if line[-1] == bid_ann_num:
            f.close()
            return line[5], line[6]

def unique_element(tb_info): # 중복요소 제거
    i = 0
    while True:
        res_list = list(filter(lambda x: tb_info['입찰공고번호'] == tb_info['입찰공고번호'][i], range(len(tb_info['입찰공고번호']))))
        if len(res_list) > 1:
            del_row(tb_info, i)
            i -= 1
            break
        i += 1
        if i >= len(tb_info['입찰공고번호']):
            break
    return tb_info

def del_row(tb_info, i): # i행을 삭제하는 함수
    for key in tb_info.keys():
        del tb_info[key]


def Custom_Table():
    # tstart = time.time()
    Init()
    # print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간

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

def extract_range(tb_info): # 예가범위 전처리
    tb_info['예가범위1'] = []
    tb_info['예가범위2'] = []
    for i in range(len(tb_info['입찰공고번호'])):
            num_list = tools.extract_number(tb_info['예가범위'][i])
            tb_info['예가범위1'].append(num_list[0])
            tb_info['예가범위2'].append(num_list[1])
    tb_info.pop('예가범위')
    return tb_info

def commaDel(tb_info):
    for i in range(len(tb_info['기초금액'])):
        tb_info['기초금액'][i] =  tb_info['기초금액'][i].replace(",", "")
    for i in range(len(tb_info['예정가격'])):
        tb_info['예정가격'][i] = tb_info['예정가격'][i].replace(",", "")
    for i in range(len(tb_info['투찰금액'])):
        tb_info['투찰금액'][i] = tb_info['투찰금액'][i].replace(",", "")
    return tb_info


if __name__ == '__main__':
    Custom_Table()
