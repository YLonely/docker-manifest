from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pickle as pic
import time
user_name = 'lwyan'
user_password = 'wuxQCeXZB8L8xyH'


def extract_pull_command(browser, pull_command):
    if pull_command is None:
        pull_command = browser.find_element_by_css_selector(
            "input[data-testid='copyPullCommandPullCommand']")
    command = pull_command.get_attribute('value').replace("docker pull ", "")
    return command


def handle_checkout_page(browser):
    # first_name_input = browser.find_element_by_css_selector(
    #     "input[name='contactFirstName']")
    # last_name_input = browser.find_element_by_css_selector(
    #     "input[name='contactLastName']")
    # company_input = browser.find_element_by_css_selector(
    #     "input[name='company']")
    # job_input = browser.find_element_by_css_selector("input[name='job']")
    # phone_input = browser.find_element_by_css_selector("input[name='phone']")
    # first_name_input.send_keys('Long')
    # last_name_input.send_keys('Long')
    # company_input.send_keys('UCAS')
    # job_input.send_keys('No')
    # phone_input.send_keys('18982770300')
    browser.implicitly_wait(3)
    try:
        pull_command = browser.find_element_by_css_selector(
            "input[data-testid='copyPullCommandPullCommand']")
        command = pull_command.get_attribute(
            'value').replace("docker pull ", "")
    except NoSuchElementException:
        check_boxes = browser.find_elements_by_css_selector(
            "input[type='checkbox']")
        for check_box in check_boxes:
            check_box.click()
        submit_button = browser.find_element_by_css_selector("button#submit")
        submit_button.click()
        command = extract_pull_command(browser, None)
    return command


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
browser.implicitly_wait(5)
browser.get("https://id.docker.com/login/?next=%2Fid%2Foauth%2Fauthorize%2F%3Fclient_id%3D43f17c5f-9ba4-4f13-853d-9d0074e349a7%26next%3D%252F%253Fref%253Dlogin%26nonce%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiI0M2YxN2M1Zi05YmE0LTRmMTMtODUzZC05ZDAwNzRlMzQ5YTciLCJleHAiOjE1NTExMDMzOTgsImlhdCI6MTU1MTEwMzA5OCwicmZwIjoiYjJLVUdJVTN6UkhvOFBGZ3ZEYnNvQT09IiwidGFyZ2V0X2xpbmtfdXJpIjoiLz9yZWY9bG9naW4ifQ.BimxRTV6YLOVPoOl2RsMgtMajuQ8b42-lkbCyZMpnfc%26redirect_uri%3Dhttps%253A%252F%252Fhub.docker.com%252Fsso%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%26state%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiI0M2YxN2M1Zi05YmE0LTRmMTMtODUzZC05ZDAwNzRlMzQ5YTciLCJleHAiOjE1NTExMDMzOTgsImlhdCI6MTU1MTEwMzA5OCwicmZwIjoiYjJLVUdJVTN6UkhvOFBGZ3ZEYnNvQT09IiwidGFyZ2V0X2xpbmtfdXJpIjoiLz9yZWY9bG9naW4ifQ.BimxRTV6YLOVPoOl2RsMgtMajuQ8b42-lkbCyZMpnfc")
id_input = browser.find_element_by_id('nw_username')
password_input = browser.find_element_by_id('nw_password')
id_input.send_keys(user_name)
password_input.send_keys(user_password)
sign_in_button = browser.find_element_by_id('nw_submit')
sign_in_button.click()
time.sleep(1)
# page_list = [i for i in range(1, 16)]
# hrefs = []
# for page in page_list:
#     url = 'https://hub.docker.com/search/?q=&type=image&image_filter=store%2Cofficial&operating_system=linux&architecture=amd64&page={0}'.format(
#         page)
#     browser.get(url)
#     search_results = browser.find_elements_by_css_selector("#searchResults a")
#     hrefs = hrefs+[search_result.get_attribute('href')
#                    for search_result in search_results]
# with open("./hrefs", "wb") as f:
#     pic.dump(hrefs, f)
# exit(0)
with open("./hrefs", 'rb') as f:
    hrefs = pic.load(f)

for href in hrefs:
    browser.get(href)
    try:
        browser.implicitly_wait(3)
        pull_command_input = browser.find_element_by_css_selector(
            "input[data-testid='copyPullCommandPullCommand']")
        command = extract_pull_command(browser, pull_command_input)
    except NoSuchElementException:
        browser.implicitly_wait(10)
        try:
            checkout_button = browser.find_element_by_css_selector(
                "button[data-testid='marketplaceCTAButton']")
            checkout_button.click()
            command = handle_checkout_page(browser)
        except NoSuchElementException:
            command = "ERROR:"+href
    with open("./patch_name.txt", 'a') as f:
        f.write(command+'\n')
