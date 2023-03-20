# 전국 대학교 위치
import pandas as pd
# pip install folium
import folium

filePath = './StudyPython/university_locations.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl', header=None) # 헤더가 없음(데이터만 존재하기 때문에 헤더 없다고 해야함 아니면 첫번째 데이터를 헤더로 인식)
df_excel.columns = ['학교명', '주소', 'lng', 'lat']

# print(df_excel)
name_list = df_excel['학교명'].to_list()
add_list = df_excel['주소'].to_list()
lng_list = df_excel['lng'].to_list()
lat_list = df_excel['lat'].to_list()

fMap = folium.Map(location=[37.553175, 126.989326], zoom_start=10)

for i in range(len(name_list)): # 446번 반복
    if lng_list[i] != 0: # 위경도 값이 0이 아니라면
        marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i],
                               icon=folium.Icon(color = 'blue'))
        marker.add_to(fMap)

fMap.save('./StudyPython/Korea_universities.html') # html 파일 만들기