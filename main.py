from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import base64
from bs4 import BeautifulSoup
import re
import os
import datetime

lag = 1
guard = 0
times = 50
try:
    driver = webdriver.Chrome()
except:
    input(print('ooops，浏览器和驱动不匹配或未安装...'))
    sys.exit()
print('欢迎使用Fuse1.0 ')


def log():
    global account, psword

    if os.path.exists('Fuse_config.json'):
        f = open('Fuse_config.json', 'r')
        psword = base64.b64decode(f.readline()).decode()
        account = base64.b64decode(f.readline()).decode()
        use = input('使用保存的账号？[' + account+'](y/n)\n')

        if use == 'y' or use == 'Y':
            pass
        else:
            os.remove('Fuse_config.json')
            log()
    else:
        account = str(input('账号plz\n'))
        psword = str(input('密码plz\n'))
        yn = input('保存密码？(y/n)\n')
        if yn == 'y' or yn == 'Y':
            print('正在保存密码...')
            try:
                byte_account = account.encode()
                byte_psword = psword.encode()
                f = open('Fuse_config.json', 'w')
                f.write(base64.b64encode(byte_psword).decode() + '\n' + base64.b64encode(byte_account).decode())
                f.close()
                print('保存成功，正在打开浏览器...')
            except:
                print('保存失败...')
        else:
            pass


def format1(sample):
    sample = str(sample)
    if sample[-2:] == '00':
        temph = int(sample[-5:-3])
        temph = temph - 1
        if len(str(temph)) == 1:
            temph = '0' + str(temph)
        else:
            temph = str(temph)
        temp = sample[-16:-12] + sample[-11:-9] + sample[-8:-6] + temph + '59' + str(60 - lag)
    else:
        tempm = int(sample[-2:])
        tempm = str(tempm - 1)
        if len(str(tempm)) == 1:
            tempm = '0' + str(tempm)
        else:
            tempm = str(tempm)
        temp = sample[-16:-12] + sample[-11:-9] + sample[-8:-6] + sample[-5:-3] + tempm + str(60 - lag)
    return temp


log()
driver.get("https://spdpo.nottingham.edu.cn/study/auth/Index?a=true")
driver.implicitly_wait(10)
print('Logging....')
driver.find_element(By.XPATH, '//*[@id="UserName"]').send_keys(account)
driver.find_element(By.XPATH, '//*[@id="Password"]').send_keys(psword)
driver.find_element(By.ID, 'btnLogin').click()
driver.get('https://spdpo.nottingham.edu.cn/study/selection')
url = input('右键目标课程按钮并复制链接粘贴到此处\n')
param = url[-36:]
print(param)
driver.get(url)
driver.implicitly_wait(5)
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
soup = str(soup)
start_pattern = re.compile('divRegStart">.{16}')
end_pattern = re.compile('报名结束时间：.{16}')
place_pattern = re.compile('地点.*</div>')
start = start_pattern.search(soup)
end = end_pattern.search(soup)
place = place_pattern.search(soup)
print(start)
start = format1(start.group())

print('已找到课程')
currenttime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
while int(start) > int(currenttime):
    currenttime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    print('Fuse Countdown:' + str(int(start) - int(currenttime)) + '...')
    time.sleep(1)

while guard <= times:
    print('---------------Fusing---------------')
    driver.execute_script(
        '$.post(\"/study/Selection/StudentSelection\", {ScheduleId: ' + '\'' + param[-36:] + '\',}, null, "json")')
    time.sleep(0.3)

input('Fuse finished, press Enter to exit...')
driver.close()
sys.exit()
