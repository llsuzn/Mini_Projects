import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverAPI import *
from urllib.request import urlopen
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/NaverAPIMovie.ui',self)
        self.setWindowIcon(QIcon('./studyPyQt/movie.png'))
        
        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblresult.doubleClicked.connect(self.tblresultDoubleClicked)

    def tblresultDoubleClicked(self):
        selected = self.tblresult.currentRow()
        url = self.tblresult.item(selected,5).text() # 더블 클릭하면 url
        webbrowser.open(url) # 웹브라우저 창에 링크가 뜬다


    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self,'경고','영화명을 입력하세요.')
            return
        else:
            api = NaverAPI() # Naver API 클래스 객체 생성
            node = 'movie' # movie로 변경하면 영화검색 가능
            display = 100

            result = api.get_naver_search(node,search,1,display)
            # print(result)
            # 테이블 위젯에 출력하는 기능
            items = result['items'] # json 결과 중 items 아래 배열만 추출
            self.makeTable(items) # 테이블 위젯에 데이터들을 할당하는 함수

    # 테이블 위젯에 데이터 display -- 네이버 영화 결과에 맞춰서 변경 : title, pubDate, director, actor, userRating, link, image
    def makeTable(self,items) -> None:
        self.tblresult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblresult.setColumnCount(7)
        self.tblresult.setRowCount(len(items)) # 현재 items 개수의 행 생성 : 100개
        self.tblresult.setHorizontalHeaderLabels(['영화제목','개봉년도','감독','배우진','평점','링크','포스터'])
        self.tblresult.setColumnWidth(0,150)
        self.tblresult.setColumnWidth(1,70) #개봉년도
        self.tblresult.setColumnWidth(3,130) #배우
        self.tblresult.setColumnWidth(4,45) #평점
        # 컬럼 데이터 수정 금지
        self.tblresult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 뉴스 ...
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자 변환 / subtitle(영어제목)은 안 가져옴
            subtitle = post['subtitle']
            title = f'{title}\n ({subtitle})'
            pubDate = post['pubDate']
            director = post['director'].replace('|',',')[:-1] # [:-1] 마지막에 있는 쉼표를 없애줌 
            actor = post['actor'].replace('|',',')[:-1]  # [:-1] : 파이썬에서만 가능하다
            userRating = post['userRating']
            link = post['link']
           
            img_url = post['image']

            # print(img_url == '') # 포스터가 없는 영화 true로 출력 받기
            if img_url != '': #포스터가 존재한다면
                data = urlopen(img_url).read() # 2진 데이터 -> 네이버 영화에 있는 이미지 읽어오기: 텍스트형태(경로정보)
                image = QImage() # 이미지 담을 수 있는 객체 생성
                image.loadFromData(data)
                # QtableWidget 이미지를 그냥 넣을 수 없음. QLabel() 집어넣은 뒤 QLabel -> QtableWidget
                imgLabel = QLabel()
                imgLabel.setPixmap(QPixmap(image))

                # 테스트 : data를 이미지로 저장
                # f = open(f'./studyPyQt/temp/image_{i+1}.png',mode='wb') # 파일 쓰기
                # f.write(data)
                # f.close()
           
            # setItem(행,열,넣을 데이터)
            self.tblresult.setItem(i,0,QTableWidgetItem(title))
            self.tblresult.setItem(i,1,QTableWidgetItem(pubDate))
            self.tblresult.setItem(i,2,QTableWidgetItem(director))
            self.tblresult.setItem(i,3,QTableWidgetItem(actor))
            self.tblresult.setItem(i,4,QTableWidgetItem(userRating))
            self.tblresult.setItem(i,5,QTableWidgetItem(link))
            # self.tblresult.setItem(i,6,QTableWidgetItem(img_url))
            if img_url != '':
                self.tblresult.setCellWidget(i,6,imgLabel)
                self.tblresult.setRowHeight(i,110) # 포스터가 있으면 쉘 높이를 늘림
            else:
                self.tblresult.setItem(i,6,QTableWidgetItem('No Poster!'))

        
    def replaceHtmlTag(self,sentence) -> str:
        result = sentence.replace('&lt','<').replace('&gt','>').replace('<b>','').replace('</b>','').replace('&apos;',"'").replace('&quot;','"')  
        # 변환 안 된 특수문자가 나타나면 밑에 추가

        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # MyApp(9일차 참고)
    ex.show()
    sys.exit(app.exec_())