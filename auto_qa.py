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
    for page_index in range(100,300,50):
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
               f'"recruitId":"{recruit_id}"}}'
    secret_str = aes.aes_encrypt(raw_data)
    data = {
        "dateFormate": int(round(time.time()) * 1000),
        "secretStr": secret_str
    }
    res = session.post(url, data=data)



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
        try:
            browser=webdriver.Firefox()
            browser.get("https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin#signin")
            browser.find_element(By.ID,"lUsername").send_keys(account)
            browser.find_element(By.ID,"lPassword").send_keys(password)
            browser.find_element(By.XPATH,'//*[@id="f_sign_up"]/div[1]/span').click()
            time.sleep(2)
            browser.find_element(By.XPATH,'//*[@id="goValidateLogin-div"]/a').click()
            time.sleep(5)
            browser.switch_to.frame('tcaptcha_iframe')
            time.sleep(0.5)
            try:
                while True:
                    target = browser.find_element(By.XPATH,'/html/body/div/div[3]/div[2]/div[1]/div[2]/img')
                    template = browser.find_element(By.XPATH,'/html/body/div/div[3]/div[2]/div[1]/div[3]/img')
                    # 获取模块的url路径
                    src1 = target.get_attribute("src")
                    src2 = template.get_attribute("src")
                    # 下载图片
                    request.urlretrieve(src1, "findPicimg1.jpg")
                    request.urlretrieve(src2, "img2.png")

                    pic1 = "findPicimg1.jpg"
                    pic2 = "img2.png"

                    # 读取图片
                    target_rgb = cv2.imread(pic1)
                    # 图片灰度化
                    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
                    # 读取模块图片
                    template_rgb = cv2.imread(pic2, 0)
                    # 匹配模块位置
                    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
                    # 获取最佳匹配位置
                    value = cv2.minMaxLoc(res)
                    # 返回最佳X坐标
                    x = value[2][0] - 80


                    w1 = cv2.imread('findPicimg1.jpg').shape[1]
                    w2 = target.size['width']

                    x = x / w1 * w2


                    track = []  # 移动轨迹
                    current = 0  # 当前位移
                    # 减速阈值
                    mid = x * 4 / 5  # 前4/5段加速 后1/5段减速

                    t = 0.5  # 计算间隔
                    v = 0  # 初速度
                    while current < x:
                        if current < mid:
                            a = random.uniform(3, 5)  # 加速度随机
                        else:
                            a = -(random.uniform(12.5, 13.5))  # 加速度随机,负数
                        v0 = v  # 初速度v0
                        v = v0 + a * t  # 当前速度
                        move = v0 * t + 1 / 2 * a * t * t  # 移动距离
                        current += move  # 当前位移
                        track.append(round(move))  # 加入轨迹


                    time.sleep(1)
                    slider = browser.find_elements(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]')[0]
                    ActionChains(browser).click_and_hold(slider).perform()

                    for x in track:
                        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()

                    ActionChains(browser).release().perform()  # 松开鼠标
                    time.sleep(2)
            except:
                pass
        except:
            pass
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
        browser.get('https://creditqa.zhihuishu.com/creditqa/login/getLoginUserInfo')

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
