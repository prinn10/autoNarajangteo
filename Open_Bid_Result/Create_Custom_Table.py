# 학습에 필요한 변수만 수집하여 저장하는 기능을 제공

# 1. 입찰공고번호 : info_tables['공고일반']['입찰공고번호']
# 2. 기초금액 : info_tables['기초금액 공개']['기초금액']
# 3. 예정가격
# 4. 예가범위
# 5. 참여업체수
# 6. 낙찰하한율
# 7. 날짜
# 8. 기초금액기준 상위개수
def Custom_Table():
    tstart = time.time()
    total_process()
    print("총 처리 시간 :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간

if __name__ == '__main__':

    total_process()
