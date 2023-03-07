import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from NaverAPU import *

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/NaverAPISearch.ui',self)
        
        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)

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
            # 리스트뷰에 출력하는 기능
            while result != None and result['display'] != 0:
                for post in result['items']: # 100개의 post 만들어짐
                    api.get_post_data(post,output) # 네이버 API class에서 처리
                    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # MyApp(9일차 참고)
    ex.show()
    sys.exit(app.exec_())