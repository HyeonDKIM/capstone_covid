import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas import Series, DataFrame
# NewsList에서 먼저 제목에 나라 이름이 들어있는 행만 추출(국가코드 변환) -> 이후 Roaming_data의 도착날짜(이후3일까지)와 게시일자가 같은경우 카운트
# 카운트 숫자들을 날짜별로 그래프로 표현 및 회귀분석(카운트를 해외에서 유입한 확진자로 가정)

# pandas 에러 제거 라인
pd.options.mode.chained_assignment = None  # default='warn'

# 뉴스 및 로밍 데이터 불러오기

data_21 = pd.read_excel('C:/Users/USER/Desktop/jin/data/3_NewsList.xls', sheet_name='List', encoding='utf-8')
data_22 = pd.read_csv('C:/Users/USER/Desktop/jin/data/3_Roaming_data.csv')

# 데이터 셋 결합
data_all_01 = pd.concat([data_21])  # 뉴스 데이터
data_all_02 = pd.concat([data_22])  # 로밍 데이터
data_all_01.reset_index(drop=True, inplace=True)  # 인덱스 초기화
data_all_02.reset_index(drop=True, inplace=True)  # 인덱스 초기화

# 로밍데이터 열별로 분할
iso = data_all_02['iso'].str.upper()  # 로밍데이터 iso 대문자로 변환
departure = data_all_02['departure']
count = data_all_02['count']

# 국가코드 데이터 불러오기
nation_code = pd.read_csv('C:/Users/USER/Desktop/jin/data/ISO3166_2.csv')
name = nation_code['Name']
code = nation_code['Code']

# 뉴스 데이터 요약
sample = data_all_01[['제목', '게시일자', '감염병명']]  # 제목 게시일자 감염병명 3가지 열 추출
sample = sample.loc[data_all_01['감염병명'].str.contains('COVID-19', na=False)]  # 감염병명이 COVID-19인 행 추출 및 결측값 제거
sample_title = sample['제목']  # 제목 열만 추출
k = data_all_02[['return', 'iso', 'departure', 'count']]

sample['게시일자'] = sample['게시일자'].str.slice(start=0, stop=10)  # 시 분 초 부분 제거
sample['게시일자'] = sample['게시일자'].str.replace(pat=r'[^A-Za-z0-9]', repl= r'', regex=True)  # 구분자 - 를 모두 제거
sample['column_int'] = pd.to_numeric(sample['게시일자'])  # 게시일자를 int형으로 변환( departure와 날짜를 계산하기 위해서)

print(sample.columns)
print(k.columns)
print(len(iso))

count_df = DataFrame(columns=("iso", "return", "count"))  # 유의미한 데이터를 담을 데이터프레임 선언
a = 0  # for문 index 다루기 위한 변수
b = 0  # for문 index 다루기 위한 변수

for i in name:
    sample2 = sample.loc[sample['제목'].str.contains(i, na=False)]  # 제목에 나라이름이 들어간 행 추출
    sample2.reset_index(drop=True, inplace=True)  # 인덱스 초기화
    print(code[a], i)
    for j in range(len(iso)):
        if code[a] == iso[j]:
            # print(sample2['column_int'])
            # print(k['departure'])
            sample2['result'] = sample2['column_int'] - k['departure'][j]
            # print('This is 첫번째 : \n', sample2['result'])
            # 게시일자와 로밍데이터의 출국 기준 3일 이내를 유효데이터로 가정
            case1 = sample2['result'] <= 10  # 조건1
            case2 = sample2['result'] >= -10  # 조건2
            sample2 = sample2[case1 & case2]  # 조건1과 2를 만족하는 행만 추출
            sample2.reset_index(drop=True, inplace=True)  # 인덱스 초기화
            # print('This is 두번째 : \n', sample2['result'])
            if len(sample2['result']) > 0:  # 위의 조건에 해당하는 로밍 데이터의 행을 새로운 데이터프레임 count_df에 삽입
                count_df.loc[b] = [k['iso'][j], k['return'][j], k['count'][j]]
                b = b + 1
    print('------------------------------------------------------')
    a = a + 1

print('################################')
print('데이터 갯수 : ', b)
print(count_df)
count_df.to_pickle('data_Result_03_10.pkl')



# 날짜별로 로밍데이터 셋에 가중치를 다르게 줘야할까 ? ..
# 코로나가 급격하게 확산된 뒤로는 로밍데이터수가 현저하게 줄어들어 데이터 셋 차이가 커짐