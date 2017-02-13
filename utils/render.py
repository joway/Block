from bs4 import BeautifulSoup
from selenium import webdriver


def render_to_html(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    return soup.contents
