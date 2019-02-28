from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle as pic
import time
from bs4 import BeautifulSoup
import json

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
with open("./hrefs", 'rb') as f:
    hrefs = pic.load(f)
search_link = "https://hub.docker.com/api/content/v1/products/images/{0}"
hrefs = [h.split("/")[-1] for h in hrefs]

for href in hrefs:
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
    plans = info['plans'][0]
    repositories = plans['repositories']
    namespace = repositories[0]['namespace']
    reponame = repositories[0]['reponame']
    tag = plans['versions'][0]['tags'][0]['value']
    created_at = info['created_at']
    created_at = created_at.replace("T", " ")
    created_at = created_at.replace("Z", "")
    updated_at = info['updated_at']
    updated_at = updated_at.replace("T", " ")
    updated_at = updated_at.replace("Z", "")
    if namespace == 'library':
        name = reponame+":"+tag
    else:
        name = namespace+"/"+reponame+":"+tag
    with open("./name.txt", 'a') as f:
        f.write(name+','+created_at+','+updated_at+','+category + '\n')
