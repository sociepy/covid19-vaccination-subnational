from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def load_driver(url):
    op = Options()
    op.add_argument("--headless")
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    return driver
