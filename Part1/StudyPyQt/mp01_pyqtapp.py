# PyQt 복습 - 직접 디자인 코딩
import sys
from PyQt5.QtWidgets import *
class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lblMessages = QLabel('메시지: ',self)
        self.lblMessages.setGeometry(10,5,300,50)

        btnOK = QPushButton('OK',self)
        btnOK.setGeometry(280,250,100,40)
        # PyQt event(signal) -> 이벤트핸들러(슬롯)
        btnOK.clicked.connect(self.btnOK_clicked)
        
        self.setGeometry(300,200,400,300)
        self.setWindowTitle('복습PyQt')
        self.show()        

    def btnOK_clicked(self):
        self.lblMessages.clear()
        self.lblMessages.setText('메시지: OK')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # MyApp(9일차 참고)
    sys.exit(app.exec_())

