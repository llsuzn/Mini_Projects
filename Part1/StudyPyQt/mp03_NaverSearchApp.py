import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverAPI import *
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/NaverAPISearch.ui',self)
        self.setWindowIcon(QIcon('./studyPyQt/newsPaper.png'))
        
        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblresult.doubleClicked.connect(self.tblresultDoubleClicked)

    def tblresultDoubleClicked(self):
        # row = self.tblresult.currentIndex().row()
        # column = self.tblresult.currentIndex().column()
        # print(row,column)
        selected = self.tblresult.currentRow()
        url = self.tblresult.item(selected,1).text() # 더블 클릭하면 url
        # print(url) # 콘솔창에  프린트
        webbrowser.open(url) # 웹브라우저 창에 링크가 뜬다


    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self,'경고','검색어를 입력하세요.')
            return
        else:
            api = NaverAPI() # Naver API 클래스 객체 생성
            node = 'news' # movie로 변경하면 영화검색 가능
            display = 100
            output = [] # 결과 담을 리스트 변수

            result = api.get_naver_search(node,search,1,display)
            # print(result)
            # 테이블 위젯에 출력하는 기능
            items = result['items'] # json 결과 중 items 아래 배열만 추출
            self.makeTable(items) # 테이블 위젯에 데이터들을 할당하는 함수

    # 테이블 위젯에 데이터 display
    def makeTable(self,items) -> None:
        self.tblresult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblresult.setColumnCount(2)
        self.tblresult.setRowCount(len(items)) # 현재 items 개수의 행 생성 : 100개
        self.tblresult.setHorizontalHeaderLabels(['기사제목','뉴스링크'])
        self.tblresult.setColumnWidth(0,310)
        self.tblresult.setColumnWidth(1,260)
        # 컬럼 데이터 수정 금지
        self.tblresult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 뉴스 ...
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자 변환
            originallink = post['originallink']
            # setItem(행,열,넣을 데이터)
            self.tblresult.setItem(i,0,QTableWidgetItem(title))
            self.tblresult.setItem(i,1,QTableWidgetItem(originallink))
        
    def replaceHtmlTag(self,sentence) -> str:
        result = sentence.replace('&lt','<').replace('&gt','>').replace('<b>','').replace('</b>','').replace('&apos;',"'").replace('&quot;','"')  
        # 변환 안 된 특수문자가 나타나면 밑에 추가

        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # MyApp(9일차 참고)
    ex.show()
    sys.exit(app.exec_())