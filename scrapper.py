import time
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from unidecode import unidecode


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
        print(f' website scanned: {scanned:.2%}')
        if scanned > 0.1:  # speed up
            scroll_increment = 300
            scroll_delay = 1


def has_specific_class_and_attribute_top_banner(tag, class_match='carousel-item', attribute='id', attribute_match='showcase-Showcase-'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])

def has_specific_class_and_attribute_second_banner(tag, class_match='BannerCard-module', attribute='id', attribute_match='main-HoldingBanner'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])


def has_specific_class_and_attribute_lower_grid(tag, class_match='grid-card', attribute='id', attribute_match='grid-card-'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])


def has_specific_class_and_attribute_lowest_carousel(tag, class_match='CategoryCarousel', attribute='id', attribute_match='main-CategoryCarousel'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])


def get_df_with_imgs(all_sections: list):
    dict_sale_type ={1: 'ofertas_principales', 2: 'ofertas_secundarias', 3: 'grid_ofertas', 4:'lo_ultimo'}
    data = []
    for idx, containers in enumerate(all_sections, start=1):
      for pos, element in enumerate(containers, start=1):
        if element.picture:
            promo = {}
            name = str(element.picture.find('img').get('alt')).lower()
            promo['name_img'] = unidecode(name)
            promo['tipo_oferta'] = dict_sale_type[idx]
            promo['position'] = pos
            url = element.picture.find('source').get('srcset')
            formatted_url = ''.join(url.split('?disable')[0])
            promo['url_img'] = formatted_url
            data.append(promo)

    df = pd.DataFrame(data)
    return df


blacklist = ['falabella', 'sodimac', 'tottus', 'linio', 'cmr', 'nosotros', 'ecosistema', 'seguros', 'puntospesos']
def flag_blacklist(row, blacklist=blacklist):
    row = str(row)
    tokens = re.findall(r"(?=("+'|'.join(blacklist)+r"))", row)
    if len(tokens) > 0:
      return 'flagged_as_blacklisted'
    else:
      return row


def main():
    ''''testing: get promotions and discounts images from home site'''
    url ='https://www.falabella.com/falabella-cl'

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-notifications')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=binary_path)
    try:
        driver.get(url)
        time.sleep(1)

        scroll_all_website(driver, scroll_increment=10, scroll_delay=1)

        # get code with lazyload-wrappers imgs loaded
        website_code = driver.page_source
        with open('webpage_source.txt', 'w', encoding='utf-8') as file:
            file.write(website_code)
        driver.quit()

        soup = BeautifulSoup(website_code, 'html.parser')
        #print(soup.prettify()) #for developing
        # sections with promos
        top_banner = soup.find_all(has_specific_class_and_attribute_top_banner)
        second_banner = soup.find_all(has_specific_class_and_attribute_second_banner)
        lower_grid = soup.find_all(has_specific_class_and_attribute_lower_grid)
        lowest_carousel = soup.find_all(has_specific_class_and_attribute_lowest_carousel)

        all_sections = [top_banner, second_banner, lower_grid, lowest_carousel]
        df_imgs = get_df_with_imgs(all_sections)

        df_imgs['name_img'] = df_imgs['name_img'].apply(lambda row: flag_blacklist(row))
        df_imgs = df_imgs[~df_imgs.name_img.isin(['flagged_as_blacklisted', ''])]  # filter out
        df_imgs = df_imgs.drop_duplicates().reset_index(drop=True)  # filter out
        df_imgs['datetime_checked'] = pd.to_datetime('today')
        print(df_imgs.head(10))
        df_imgs.to_csv('df_promos_retail.csv')

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()