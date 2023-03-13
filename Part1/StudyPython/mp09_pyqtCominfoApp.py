import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon 여기있음
from PyQt5.QtCore import * # Qt.white 여기 있음
import psutil
import socket
import requests # pip install requests
import re

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/cominfo.ui',self)
        self.setWindowTitle('QrCode 생성앱 v0.2')
        self.setWindowIcon(QIcon('./StudyPython/settings.png'))

        self.btnRefresh.clicked.connect(self.btnRefreshClicked)
        self.initInfo()

    def btnRefreshClicked(self):
        self.initInfo()        

    def initInfo(self):
        cpu = psutil.cpu_freq() # cpu 주파수 정보 : 3408
        cpu_ghz = round(cpu.current / 1000, 2) # 3.41
        self.lblCPU.setText(f'{cpu_ghz:.2f} GHz')
        
        core = psutil.cpu_count(logical=False) # 코어 갯수 : 4개
        logical = psutil.cpu_count(logical=True) # 논리 프로세서 갯수
        self.lblCore.setText(f'{core} 개 / 논리 프로세서 {logical} 개')

        memory = psutil.virtual_memory() # 메모리 용량
        mem_total = round(memory.total / 1024**3 )
        self.lblMemory.setText(f'{mem_total} GB')

        disks = psutil.disk_partitions() # 디스크 갯수
        for disk in disks:
            if disk.fstype == 'NTFS':
                du = psutil.disk_usage(disk.mountpoint)
                du_total = round(du.total / 1024**3 )
                msg = f'{disk.mountpoint} {disk.fstype} - {du_total} GB'
                
                self.lblDisk.setText(msg) 
                break # c 드라이브만 나오게 됨
        
        # print(psutil.net_if_addrs())
        in_addr = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 내부아이피
        in_addr.connect(('www.google.com',443))
        self.lblInnerNet.setText((in_addr.getsockname()[0]))

        req = requests.get('http://ipconfig.kr') # 외부아이피
        out_addr = req.text[req.text.find('<font color=red>')+17:req.text.find('</font><br>')]
        self.lblExtraNet.setText(out_addr)

        net_stat = psutil.net_io_counters() # 전송상태
        sent = round(net_stat.bytes_sent / 1024**2 ,1)#메가바이트
        recv = round(net_stat.bytes_recv / 1024**2 ,1)
        self.lblNetStat.setText(f'송신 - {sent} MB / 수신 - {recv} MB')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())     