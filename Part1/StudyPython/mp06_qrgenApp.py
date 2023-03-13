# qr 생성앱
import qrcode

qr_data = 'https://www.python.org'
qr_img = qrcode.make(qr_data)

qr_img.save('./StudyPython/site.png')

# qrcode.run_example(data='https://www.naver.com')
