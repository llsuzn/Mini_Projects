import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon 여기있음
from PyQt5.QtCore import * # Qt.white 여기 있음
import qrcode       

class qtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/QrcodeApp.ui',self)
        self.setWindowTitle('QrCode 생성앱 v0.1')
        self.setWindowIcon(QIcon('./StudyPython/qr-code.png'))
    
        # 시그널/슬롯함수
        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked) # 엔터

    def btnQrGenClicked(self):
        data = self.txtQrData.text()

        if data == '':
            QMessageBox.warning(self,'경고','데이터를 입력하세요.')
            return
        else:
            qr_img = qrcode.make(data)
            qr_img.save('./StudyPython/site.png')

            img = QPixmap('./StudyPython/site.png')
            self.lblQrCode.setPixmap(QPixmap(img).scaledToWidth(300))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())      