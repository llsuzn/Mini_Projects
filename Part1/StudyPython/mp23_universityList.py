# 전국 대학교 지도 표시
# pip install pandas
import pandas as pd

filePath = './StudyPython/university_list_2020.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl')
df_excel.columns = df_excel.loc[4].tolist()
df_excel = df_excel.drop(index=list(range(0,5))) # 실제 데이터 위에 필요없는 행을 날려버림

print(df_excel.head()) # 상위 다섯개 리스트만 프린트

print(df_excel['학교명'].values) # 학교명인 컬럼만 출력
print(df_excel['주소'].values) # 주소 컬럼만 출력