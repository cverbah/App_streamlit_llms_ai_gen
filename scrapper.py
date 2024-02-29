import time
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib
import requests

def main():
    ''''testing'''
    url ='https://www.falabella.com/falabella-cl'

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-notifications')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=binary_path)
    try:
        driver.get(url)
        time.sleep(1)
        page_height = driver.execute_script("return document.body.scrollHeight")

        # for loading all images (lazy load wrapper)
        # define the scroll increment and delay between scrolls
        scroll_increment = 100
        scroll_delay = 0.25

        # wcroll from top to bottom
        current_position = 0
        while current_position < page_height:

            driver.execute_script(f"window.scrollTo(0, {current_position});") # Scroll down by the scroll_increment
            time.sleep(scroll_delay)

            current_position += scroll_increment # update the current position

        # get code with loaded items
        website_code = driver.page_source
        with open('webpage_source.txt', 'w', encoding='utf-8') as file:
            file.write(website_code)
        driver.quit()

        soup = BeautifulSoup(website_code, 'html.parser')
        print(soup.prettify())

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()