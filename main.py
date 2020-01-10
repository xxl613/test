import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_one_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        return response.text
    else:
        return None


def main():
    url = "https://maoyan.com/board/4"
    browser = webdriver.Chrome()
    browser.get(url)
    wait = WebDriverWait(browser, 10)   # 指定页面等待时间
    print(browser.get_cookies())




    browser.close()

main()