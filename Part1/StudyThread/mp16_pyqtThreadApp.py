# 스레드 사용 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon 여기있음
from PyQt5.QtCore import * # Qt.white 여기 있음
import time

MAX = 10000

class BackgroundWorker(QThread): # pyqt5 스레드를 위한 클래스 존재
    procChanged = pyqtSignal(int) # 커스텀 시그널

    def __init__(self, count = 0, parent = None) -> None:
        super().__init__()
        self.main = parent
        self.working = False # 스레드 동작여부
        self.count = count 

    def run(self): # thread.start() --> run() 대신 실행
        while self.working:
            if self.count <= MAX:
                self.procChanged.emit(self.count) # 시그널을 내보냄(emit)
                self.count += 1 # 값 증가만
                time.sleep(0.0001) # 0.0000001 처럼 세밀하게 하면 GUI처리를 제대로 못 함
            else:
                self.working = False # 멈춤                

class qtApp(QWidget): # 전체동작
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui',self)
        self.setWindowTitle('스레드 앱 v0.5')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)
        # 스레드 생성
        self.worker = BackgroundWorker(parent=self,count=0)
        # 백그라운드 워커에 있는 시그널을 접근 슬롯함수
        self.worker.procChanged.connect(self.procUpdated)
        self.pgbTask.setRange(0,MAX)

    # @pyqtSlot(int) : 데코레ㅔ이션
    def procUpdated(self, count):
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')

    def btnStartClicked(self):
        self.worker.start() # 스레드 클래스 run()실행
        self.worker.working = True
        self.worker.count = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())             