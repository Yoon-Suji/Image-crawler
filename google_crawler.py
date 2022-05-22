from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
import pandas as pd

## 96장 정도에서 중복생김. 스크롤을 끝까지 내리지 않고 이미 수집했던 사진을 다시 수집함. -> SCROLL_PAUSE_TIME 조정해서 해결
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def crawling_img(name):
    driver = webdriver.Chrome('C:\chromedriver.exe')
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element_by_name("q")
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    # 도구 > 이미지 크기 > 큼
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[2]/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[1]/div/div[1]/div/div[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[3]/div/a[2]').click()
    time.sleep(1)
    
    #
    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")  # 브라우저의 높이를 자바스크립트로 찾음
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 브라우저 끝까지 스크롤을 내림
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height

    imgs = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    dir = "C:/Users/SAMSUNG/Desktop/2021 졸프/fedi/images" + "/" + name

    createDirectory(dir) #폴더 생성
    count = 1
    for img in imgs:
        try:
            img.click()
            time.sleep(2)
            imgUrl = driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img').get_attribute(
                "src")
            path = "C:\\Users\\SAMSUNG\\Desktop\\2021 졸프\\fedi\\images\\" + name + "\\" #만든 폴더에 저장
            urllib.request.urlretrieve(imgUrl, path + name + str(count) + ".jpg")
            count = count + 1
            print(count) #Debug
            if count >= 150:
                break
        except:
            pass
    driver.close()
df = pd.read_excel('C:/Users/SAMSUNG/Desktop/2021 졸프/fedi/celeb_name.xlsx', header=None)

idols = list(df[1])

for idol in idols[48:]:
    crawling_img(idol)