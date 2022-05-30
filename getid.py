import requests
from zhs_api import *
import time,random
from bs4 import BeautifulSoup

def sharecourse_info(status=0, page_no=1, page_size=5):
    url = 'https://onlineservice-api.zhihuishu.com/gateway/t/v1/student/course/share/queryShareCourseInfo'
    aes = AESEncrypt(key=HOME_PAGE_AES_KEY, iv=ZHS_AES_IV, mode=ZHS_AES_MODE)
    raw_data = f'{{"status":{status},"pageNo":{page_no},"pageSize":{page_size}}}'
    secret_str = aes.aes_encrypt(raw_data)
    data = {"secretStr": secret_str}
    res = session.post(url, data=data)
    for i in range(len(res.json().get('result').get('courseOpenDtos'))):
        if name == res.json().get('result').get('courseOpenDtos')[i].get('courseName'):
            courseId=res.json().get('result').get('courseOpenDtos')[i].get('courseId')
            recruitId=res.json().get('result').get('courseOpenDtos')[i].get('recruitId')
            return courseId,recruitId





