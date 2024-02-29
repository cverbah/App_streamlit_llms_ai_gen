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
import re

## functions ###

def scroll_all_website(driver, scroll_increment=100, scroll_delay=0.25): # scroll from top to bottom
    page_height = driver.execute_script("return document.body.scrollHeight")
    print(f'page length: {page_height}')
    current_position = 0

    while current_position < page_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_delay)

        current_position += scroll_increment
        scanned = round(current_position/page_height, 2)
        print(f'scanned: {scanned}')
        if scanned > 0.1:  # speed up
            scroll_increment = 300
            scroll_delay = 1


def get_imgs(soup):
    elements = soup.find_all('div', attrs={"class": "lazyload-wrapper"})
    all_imgs = []
    for element in elements:
        if element.picture:
            element_dict = {}
            element_dict['name_img'] = element.picture.find('img').get('alt')
            element_dict['url_img'] = element.picture.find('source').get('srcset')
            all_imgs.append(element_dict)

    df = pd.DataFrame(all_imgs)
    return df


blacklist = ['falabella', 'sodimac', 'tottus', 'cmr', 'nosotros', 'ecosistema', 'seguros', 'puntospesos']
def clean_name(row, blacklist=blacklist):
    row = str(row)
    tokens = re.findall(r"(?=("+'|'.join(blacklist)+r"))", row)
    if len(tokens) > 0:
      return 'blacklisted'
    else:
      return row


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

        scroll_all_website(driver, scroll_increment=20, scroll_delay=1)

        # get code with lazyload-wrappers imgs loaded
        website_code = driver.page_source
        with open('webpage_source.txt', 'w', encoding='utf-8') as file:
            file.write(website_code)
        driver.quit()

        soup = BeautifulSoup(website_code, 'html.parser')
        #print(soup.prettify()) #for developing
        df_imgs = get_imgs(soup)
        df_imgs['name_img'] = df_imgs['name_img'].apply(lambda row: clean_name(row))
        df_imgs = df_imgs[df_imgs.name_img != 'blacklisted'].reset_index(drop=True)  # filter out
        print(df_imgs.head(10))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()