# 주소록 GUI 프로그램 - MySQL 연동
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql

class qtApp(QMainWindow):
    conn = None

    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/AddressBook.ui',self)
        self.setWindowIcon(QIcon('./studyPyQt/Addressicon.png'))

        self.initDB() # DB초기화

    def initDB(self):
        self.conn = pymysql.connect(host='localhost',user='root',password='815301',
                                    db='miniproject',charset='utf8')
        cur = self.conn.cursor()
        query = 'SELECT * FROM addressbook'
        cur.execute(query)
        rows = cur.fetchall()
        
        print(rows) # 콘솔창에 주소 출력
        self.conn.close() # 프로그램 종료할 때

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # MyApp(9일차 참고)
    ex.show()
    sys.exit(app.exec_())        