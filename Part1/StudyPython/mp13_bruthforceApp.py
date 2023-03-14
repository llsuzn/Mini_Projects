# 암호해제 앱 (무차별 대입 공격)
import itertools
import time
import zipfile

passwd_string = '0123456789' 
# 패스워드에 영문자도 들어있다면 
# passwd_string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

file = zipfile.ZipFile('./studyPython/passwordApp.zip')
isFind = False # 암호를 찾았는지 물어봄

for i in range(4,5):
    attempts = itertools.product(passwd_string, repeat=i)
    for attempts in attempts:
        try_pass = ''.join(attempts)
        print(try_pass)
        time.sleep(0.000005)
        try:
            file.extractall(pwd=try_pass.encode(encoding='utf-8'))
            print(f'암호는 {try_pass}입니다')
            isFind = True; break
        except:
            pass            

    if isFind == True: break