# 주소록 GUI 프로그램 - MySQL 연동
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql

class qtApp(QMainWindow):
    conn = None
    curIdx = 0 # -- 4 (저장 시 데이터 중복 없애기 위해서) 현재 데이터의 PK


    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/AddressBook.ui',self)
        self.setWindowIcon(QIcon('./studyPyQt/Addressicon.png'))
        self.setWindowTitle('주소록')

        self.initDB() # DB초기화

        # 버튼 시그널/슬롯함수 지정 
        self.btnNew.clicked.connect(self.btnNewClicked) # -- 1
        self.btnSave.clicked.connect(self.btnSaveClicked) # -- 2
        self.tblAddress.doubleClicked.connect(self.tblAddressDoubleClicked) # -- 3
        self.btnDel.clicked.connect(self.btnClicked) # -- 5 : 삭제 버튼

    def btnNewClicked(self): # 신규버튼 누르면 -- 1
        # 라인 에디트 내용 삭제 후 이름에 포커스 맞춤
        self.txtName.setText('')        
        self.txtPhone.setText('')        
        self.txtEmail.setText('')        
        self.txtAddress.setText('')        
        self.txtName.setFocus()
        self.curIdx = 0 # -- 4 : 0은 진짜 신규! 
        print(self.curIdx)

    def btnSaveClicked(self): # 저장 -- 2
        FullName = self.txtName.text()
        PhoneNum = self.txtPhone.text()
        Email = self.txtEmail.text()
        Address = self.txtAddress.text()

        # print(FullName,PhoneNum,Email,Address)
        # 이름과 번호를 입력하지 않으면 알람
        if FullName == '' or PhoneNum == '':
            QMessageBox.warning(self,'주의','이름과 전화번호를 입력하세요.')
            return # 진행 불가
        else:
            self.conn = pymysql.connect(host='localhost',user='root',password='815301',
                                    db='miniproject',charset='utf8')
            
            if self.curIdx == 0: # -- 4 : 신규입력시
                # 네개 변수값 받아서 INSERT 쿼리문 만들기
                query = '''INSERT INTO addressbook (FullName,PhoneNum,Email,Address)
				            VALUES(%s, %s, %s, %s)'''
            else: # -- 5 : 데이터 수정(저장)
                query = '''UPDATE addressbook
                              SET FullName = %s
                                , PhoneNum = %s
                                , Email = %s
                                , Address = %s
                            WHERE idx = %s'''

            cur = self.conn.cursor()
            
            if self.curIdx == 0: # -- 4
                cur.execute(query,(FullName,PhoneNum,Email,Address))
            else:
                cur.execute(query,(FullName,PhoneNum,Email,Address,self.curIdx))

            self.conn.commit()
            self.conn.close()

            #저장성공 메세지
            if self.curIdx == 0: # -- 4
                QMessageBox.about(self,'성공','저장 성공했습니다!')
            else:
                QMessageBox.about(self,'성공','변경 성공했습니다!')

            # QTableWidget 새 데이터가 출력되도록
            self.initDB()
            # 입력창 내용 없어져
            self.btnNewClicked()

    def tblAddressDoubleClicked(self): # -- 3
        rowIndex = self.tblAddress.currentRow()
        self.txtName.setText(self.tblAddress.item(rowIndex,1).text()) # 더블클릭하면 이름 정보 입력칸에 이름이 뜬다            
        self.txtPhone.setText(self.tblAddress.item(rowIndex,2).text()) # 전화번호          
        self.txtEmail.setText(self.tblAddress.item(rowIndex,3).text()) # 이메일            
        self.txtAddress.setText(self.tblAddress.item(rowIndex,4).text()) # 주소            

        self.curIdx = int(self.tblAddress.item(rowIndex,0).text()) # -- 4
        print(self.curIdx)

    def btnClicked(self): # -- 5
        if self.curIdx == 0:
            QMessageBox.warning(self,'경고','삭제할 데이터를 선택하세요')
            return # 함수 종료
        else:
            reply = QMessageBox.question(self,'확인','정말로 삭제하시겠습니까?',QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return # 함수 빠져나감
            
            self.conn = pymysql.connect(host='localhost',user='root',password='815301',
                                        db='miniproject',charset='utf8')
            query = 'DELETE FROM addressbook WHERE Idx = %s'
            cur = self.conn.cursor()
            cur.execute(query,(self.curIdx))

            self.conn.commit()
            self.conn.close()

            QMessageBox.about(self,'성공','데이터를 삭제했습니다.')

            self.initDB()
            self.btnNewClicked()

    def initDB(self):
        self.conn = pymysql.connect(host='localhost',user='root',password='815301',
                                    db='miniproject',charset='utf8')
        cur = self.conn.cursor()
        query = '''SELECT idx
	                    , FullName
                        , PhoneNum
                        , Email
                        , Address
                     FROM addressbook'''
        cur.execute(query)
        rows = cur.fetchall()
        
        # print(rows) # 콘솔창에 주소 출력
        self.makeTable(rows)
        self.conn.close() # 프로그램 종료할 때

    def makeTable(self,rows):
        self.tblAddress.setColumnCount(5) # 0, 열 갯수
        self.tblAddress.setRowCount(len(rows)) # 0, 행 갯수
        self.tblAddress.setSelectionMode(QAbstractItemView.SingleSelection) # 1. 단일선택
        self.tblAddress.setHorizontalHeaderLabels(['번호','이름','핸드폰','이메일','주소']) # 1. 열제목
        self.tblAddress.setColumnWidth(0,0) # 번호(idx)는 숨김
        self.tblAddress.setColumnWidth(1,70)
        self.tblAddress.setColumnWidth(2,100)
        self.tblAddress.setColumnWidth(3,200)
        self.tblAddress.setColumnWidth(4,194)
        self.tblAddress.setEditTriggers(QAbstractItemView.NoEditTriggers) # 1. 컬럼 수정 금지

        for i , row in enumerate(rows):
            # row[0]~row[4] 까지 
            idx = row[0]
            FullName = row[1]
            PhoneNum = row[2]
            Email = row[3]
            Address = row[4]

            self.tblAddress.setItem(i,0,QTableWidgetItem(str(idx)))
            self.tblAddress.setItem(i,1,QTableWidgetItem(FullName))
            self.tblAddress.setItem(i,2,QTableWidgetItem(PhoneNum))
            self.tblAddress.setItem(i,3,QTableWidgetItem(Email))
            self.tblAddress.setItem(i,4,QTableWidgetItem(Address))

        self.stbCurrent.showMessage(f'전체 주소록 :{len(rows)}개')            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # MyApp(9일차 참고)
    ex.show()
    sys.exit(app.exec_())        