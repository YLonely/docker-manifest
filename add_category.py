from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle as pic
import time
from bs4 import BeautifulSoup
import json
user_name = 'lwyan'
user_password = 'wuxQCeXZB8L8xyH'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
with open("./hrefs", 'rb') as f:
    hrefs = pic.load(f)
search_link = "https://hub.docker.com/api/content/v1/products/images/{0}"
hrefs = [h.split("/")[-1] for h in hrefs]
with open('./new_name.txt') as f:
    lines = f.readlines()

i = 0
for href in hrefs[:351]:
    url = search_link.format(href)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    cc = soup.select('pre')[0]
    info = json.loads(cc.string)
    categories = info['categories']
    if len(categories) == 0:
        category = "unknown"
    else:
        category = categories[0]['name']
    with open("./new_name2.txt", 'a') as f:
        f.write(lines[i].replace('\n', '')+','+category + '\n')
    i += 1
