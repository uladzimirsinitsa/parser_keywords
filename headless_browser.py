
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup


def get_text_from_url(url: str):
    service = Service(executable_path=r'/usr/src/app/chromedriver')
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html5lib')

    return soup.find('body').text