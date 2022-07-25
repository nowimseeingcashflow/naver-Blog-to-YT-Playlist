import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
import emoji

def remove_emoji(text): 
    return emoji.replace_emoji(text, '')

blogUrl=input("URL을 입력해주세요 : ")
res= requests.get(blogUrl)
res.raise_for_status()

soup=BeautifulSoup(res.text, "lxml")

realurl="https://blog.naver.com"+soup.find("iframe")["src"]

res=requests.get(realurl)
res.raise_for_status()

soupie=BeautifulSoup(res.text, "lxml")
ln = soupie.find("div", attrs={"class", "pcol1"}).text.strip()
ln = remove_emoji(ln)

home=soupie.find("div", attrs={"class":"se-main-container"})
urls=home.find_all("script")
makeList=[]

for url in urls:
    onoff=0
    music=""
    
    d=re.search("inputUrl", str(url))
    if not d:
        continue

    for i in str(url)[d.end()+3:]:
        if i!='h' and onoff==0:
            continue

        onoff=1

        if i==',':
            break
        
        music+=i

    makeList.append(music)

#webdriver은 알아서 ~

#디버그 모드
# C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
#이걸 win+r 해서 켜보자

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(options=chrome_options)

browser.get(makeList[0])
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[2]')))
if len(browser.find_elements(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[3]'))!=0:
    browser.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[3]').click()

else:
    browser.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[2]').click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="endpoint"]/tp-yt-paper-item')))
browser.find_element(By.XPATH, '//*[@id="endpoint"]/tp-yt-paper-item').click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-add-to-playlist-renderer/div[3]/ytd-add-to-playlist-create-renderer/div/yt-text-input-form-field-renderer/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input')))
listName = browser.find_element(By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-add-to-playlist-renderer/div[3]/ytd-add-to-playlist-create-renderer/div/yt-text-input-form-field-renderer/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input')
listName.send_keys(ln)
browser.find_element(By.XPATH, '//*[@id="dropdown-trigger"]').click()
#WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="entries"]/ytd-privacy-dropdown-item-renderer[1]')))
time.sleep(1)
browser.find_element(By.XPATH, '//*[@id="entries"]/ytd-privacy-dropdown-item-renderer[1]').click()
browser.find_element(By.XPATH, '//*[@id="actions"]/ytd-button-renderer').click()

for yturl in makeList[1:]:
    browser.get(yturl)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[2]')))
    if len(browser.find_elements(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[3]'))!=0:
        browser.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[3]').click()

    else:
        browser.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-button-renderer[2]').click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkboxContainer"]')))
    names = browser.find_elements(By.XPATH, '//*[@id="checkboxLabel"]')
    gotcha = 0
    for idx, name in enumerate(names):
        if str(name.text).strip() == ln.strip():
            gotcha = idx
            break

    browser.find_elements(By.XPATH, '//*[@id="checkboxContainer"]')[gotcha].click()
    
    time.sleep(1)