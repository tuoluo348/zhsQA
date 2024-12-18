from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,random,requests,os,cv2
from selenium.webdriver import ActionChains
from tqdm import tqdm
from urllib import request
import getid
from zhs_api import *

def get_qid(page_index=0, page_size=50):
    lst=[]
    url='https://creditqa-api.zhihuishu.com/creditqa/gateway/t/v1/web/qa/getRecommendList'
    aes = AESEncrypt(key=QA_AES_KEY, iv=ZHS_AES_IV, mode=ZHS_AES_MODE)
    for page_index in range(800,1200,50):
        raw_data = f'{{"courseId":"{course_id}","pageIndex":{page_index},' \
                       f'"pageSize":{page_size},"recruitId":"{recruit_id}"}}'
        secret_str = aes.aes_encrypt(raw_data)
        data = {
                "dateFormate": int(round(time.time()) * 1000),
                "secretStr": secret_str
            }

        res = session.post(url, data=data)
        a=res.json().get('rt').get('questionInfoList')
        for i in range(len(a)):
            if res.json().get('rt').get('questionInfoList')[i].get('answerNum')>0:
                b=res.json().get('rt').get('questionInfoList')[i].get('questionId')
                lst.append(b)
    return lst

def get_text(qid,page_index=0, page_size=20):
    lst=[]
    url = 'https://creditqa-api.zhihuishu.com/creditqa/gateway/t/v1/web/qa/getAnswerInInfoOrderByTime'
    aes = AESEncrypt(key=QA_AES_KEY, iv=ZHS_AES_IV, mode=ZHS_AES_MODE)
    raw_data = f'{{"questionId":"{qid}","sourceType":"2","courseId":"{course_id}",' \
               f'"recruitId":"{recruit_id}","pageIndex":{page_index},"pageSize":{page_size}}}'
    secret_str = aes.aes_encrypt(raw_data)
    data = {
        "dateFormate": int(round(time.time()) * 1000),
        "secretStr": secret_str
    }
    res = session.post(url, data=data)
    a=res.json().get('rt').get('answerInfos')
    for i in range(len(a)):
        b=res.json().get('rt').get('answerInfos')[i].get('answerContent')
        lst.append(b)
    n=random.randint(0,len(lst)-1)
    return lst[n]

def suss(qid,text):
    url = 'https://creditqa-api.zhihuishu.com/creditqa/gateway/t/v1/web/qa/saveAnswer'
    aes = AESEncrypt(key=QA_AES_KEY, iv=ZHS_AES_IV, mode=ZHS_AES_MODE)
    raw_data = f'{{"annexs":"[]","qid":"{qid}","source":"2","aContent":"{text}","courseId":"{course_id}",' \
               f'"recruitId":"{recruit_id}","saveSource":1}}'
    secret_str = aes.aes_encrypt(raw_data)
    data = {
        "dateFormate": int(round(time.time()) * 1000),
        "secretStr": secret_str
    }
    res = session.post(url, data=data)
    if res.json().get('msg')=='超过最大提交数':
        input('出现验证码')


def q1():
    lsts=[]
    with open('user.txt','r',encoding='utf-8') as fp:
        uu=fp.read().splitlines()
    for i in uu:
        i=i.replace('\t',' ')
        i=i.split(' ')
        lsts.append(i)

    for i in tqdm(range(len(lsts))):
        try:
            account=lsts[i][1]
            password=lsts[i][2]
            
            browser=webdriver.Chrome()
            browser.get("https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin#signin")
            time.sleep(15)
                
            browser.get('https://onlineweb.zhihuishu.com/onlinestuh5')
            delay = 10
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'course-menu-w')))
            try:
                d=browser.find_element(By.XPATH,'//*[@id="student-page"]/div[4]')
                browser.execute_script('arguments[0].removeAttribute("Class")', d);
            except:
                pass
            break
            #browser.find_element(By.XPATH,'//*[@id="sharingClassed"]/div[2]/ul[1]/div/dl/dt/div[2]/ul/li[3]/a/div').click()
            #time.sleep(5)
            #browser.get('https://creditqa.zhihuishu.com/creditqa/login/getLoginUserInfo')

            cookies = browser.get_cookies()

            session = requests.Session()
            session.headers.clear()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            browser.quit()
            getid.session=session
            getid.name=lsts[i][3]
            course_id,recruit_id=getid.sharecourse_info(status=0, page_no=1, page_size=5)
            q_num=len(get_qid())
            for i in tqdm(range(q_num)):
                try:
                    suss(get_qid()[i],get_text(get_qid()[i]))
                    time.sleep(2)
                except:
                    pass
        except:
            with open("error.txt","a") as fp:
                fp.write("a "+account+" "+password+"\t"+lsts[i][3])
                fp.write("\n")
            browser.quit()
            continue

print(1)
browser=webdriver.Chrome()
browser.get("https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin#signin")
kcname=input('登陆后输入课程名称:')
browser.get('https://onlineweb.zhihuishu.com/onlinestuh5')
delay = 10
myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'course-menu-w')))
try:
    d=browser.find_element(By.XPATH,'//*[@id="student-page"]/div[4]')
    browser.execute_script('arguments[0].removeAttribute("Class")', d);
except:
    pass

browser.find_element(By.XPATH,'//*[@id="sharingClassed"]/div[2]/ul[1]/div/dl/dt/div[2]/ul/li[3]/a/div').click()
time.sleep(5)
#browser.get('https://creditqa.zhihuishu.com/creditqa/login/getLoginUserInfo')

cookies = browser.get_cookies()

session = requests.Session()
session.headers.clear()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

getid.session=session
getid.name=kcname
course_id,recruit_id=getid.sharecourse_info(status=0, page_no=1, page_size=5)
q_num=len(get_qid())
for i in tqdm(range(q_num)):
    try:
        suss(get_qid()[i],get_text(get_qid()[i]))
        time.sleep(2)
    except:
        pass

