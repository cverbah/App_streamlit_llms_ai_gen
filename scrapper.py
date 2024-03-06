import time
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from unidecode import unidecode
import sys

## functions ###


def scroll_all_website(driver, scroll_increment=100, scroll_delay=0.25,
                       increment_speed_up=300, delay_speed_up=1): # scroll from top to bottom

    page_height = driver.execute_script("return document.body.scrollHeight")
    print(f'page length: {page_height}')
    current_position = 0

    while current_position < page_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_delay)

        new_page_height = driver.execute_script("return document.body.scrollHeight")
        if page_height < new_page_height:
            print(f'page length updated to: {new_page_height}')
            page_height = new_page_height

        current_position += scroll_increment
        scanned = round(current_position/page_height, 2)
        print(f' website scanned: {scanned:.2%}')
        if scanned > 0.1:  # speed up
            scroll_increment = increment_speed_up
            scroll_delay = delay_speed_up


## lider - supermarket
def has_specific_class_and_attribute_top_banner_lider_supermarket(tag, class_match='banners-home', attribute='id', attribute_match='home-banner-'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])


def get_top_banner_promos_lider_supermarket(soup, tipo_oferta='ofertas_principales'):
    top_banner = soup.find_all(has_specific_class_and_attribute_top_banner_lider_supermarket)
    data = []
    for element in top_banner:
      promo = {}
      name = str(element.find('img').get('alt')).lower()
      img_url = element.find('img').get('src')
      pos = int(name.split('-')[-1]) + 1

      promo['nombre_promocion'] = name
      promo['tipo_oferta'] = tipo_oferta
      promo['posicion'] = pos
      promo['url_img'] = img_url
      data.append(promo)

    df = pd.DataFrame(data).drop_duplicates()
    df = df.sort_values(by='posicion').reset_index(drop=True)
    return df


def has_specific_class_and_attribute_grid_lider_supermarket(tag, class_match='limited-time-sales', attribute='id', attribute_match='grid'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])

def has_specific_class_and_attribute_grid_banner_lider_supermarket(tag, class_match='line-breaker', attribute='id', attribute_match='line-breakers'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])


def get_grid_promos_lider_supermarket(soup, tipo_oferta='grid_ofertas'):
    grid = soup.find_all(has_specific_class_and_attribute_grid_lider_supermarket)
    grid_banner = soup.find_all(has_specific_class_and_attribute_grid_banner_lider_supermarket)
    data = []
    for element in grid:  # grid
        promo = {}
        name = str(element.get('id')).lower()
        img_url = element.get('style').split('url("')[1].split('")')[0]
        pos = int(name.split('-')[0].replace('grid', ''))

        promo['nombre_promocion'] = name
        promo['tipo_oferta'] = tipo_oferta
        promo['posicion'] = pos
        promo['url_img'] = img_url
        data.append(promo)

    for element in grid_banner:  # lower banner grid
        promo = {}
        name = str(element.get('id')).lower()
        img_url = element.find('img').get('src')
        pos = pos + 1

        promo['nombre_promocion'] = name
        promo['tipo_oferta'] = tipo_oferta
        promo['posicion'] = pos
        promo['url_img'] = img_url
        data.append(promo)

    df = pd.DataFrame(data).drop_duplicates()
    df = df.sort_values(by='posicion').reset_index(drop=True)

    return df


def has_specific_class_bottom_offers_lider_supermarket(tag, class_match='CampaignHomeStyledComponents__OffersBannerSection'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class']))


def has_specific_class_bottom_highlighted_lider_supermarket(tag, class_match='CampaignHomeStyledComponents__InspirationalSection'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class']))


def get_lowest_offers_lider_supermarket(soup, tipo_oferta='ofertas_final_pag'):
    bottom_offers = soup.find_all(has_specific_class_bottom_offers_lider_supermarket)
    destacados_lider = soup.find_all(has_specific_class_bottom_highlighted_lider_supermarket)

    lowest_imgs = [container.find_all("img") for container in bottom_offers][0]
    lowest_imgs.extend([container.find_all("img") for container in destacados_lider][0])
    data = []
    for pos, element in enumerate(lowest_imgs, start=1):
        promo = {}
        name = str(element.get('alt')).lower() + '-' + str(pos)
        img_url = element.get('src')

        promo['nombre_promocion'] = name
        promo['tipo_oferta'] = tipo_oferta
        promo['posicion'] = pos
        promo['url_img'] = img_url
        data.append(promo)

    df = pd.DataFrame(data)
    return df


## paris scrapping
def get_top_banner_promos_paris(soup, tipo_oferta='ofertas_principales', class_tag="flex-none rounded-lg relative"):
    paris_top_banner = soup.find_all("div", {"class": class_tag})
    data = []
    for pos, element in enumerate(paris_top_banner, start=1):
        if element.picture:
            promo = {}
            name = str(element.find('img').get('alt')).lower().replace('en paris.cl', '').replace('paris', '')
            img_url = element.find('source').get('srcset')

            promo['nombre_promocion'] = unidecode(name)
            promo['tipo_oferta'] = tipo_oferta
            promo['posicion'] = pos
            promo['url_img'] = img_url
            data.append(promo)
    df = pd.DataFrame(data)
    return df


def get_grid_promos_paris(soup, tipo_oferta='grid_ofertas', class_tag="cursor-pointer relative"):

    paris_grid = soup.find_all("a", {"class": class_tag})
    data = []
    position = 1
    for element in paris_grid:
      if element.picture:
        promo = {}
        name = str(element.find('img').get('alt')).lower().replace('en paris.cl','').replace('paris','')
        img_url = element.find('source').get('srcset')
        promo['nombre_promocion'] = unidecode(name)
        promo['tipo_oferta'] = tipo_oferta
        promo['posicion'] = position
        promo['url_img'] = img_url
        data.append(promo)
        position += 1
    df = pd.DataFrame(data)
    return df


def has_specific_class_and_attribute_lowest_carousel_paris(tag, class_match='splide__slide', attribute='id', attribute_match='splide'):
    return (tag.has_attr('class') and any(class_match in cls for cls in tag['class'])) and \
           (tag.has_attr(attribute) and attribute_match in tag[attribute])


def get_lowest_carousel_paris(soup, tipo_oferta='lo_ultimo'):
    lowest_carousel = soup.find_all(has_specific_class_and_attribute_lowest_carousel_paris)
    data = []
    position = 1
    for pos, element in enumerate(lowest_carousel, start=1):
        promo_data = element.find_all('img')
        for i in promo_data:
            promo = {}
            name = str(i.get('alt')).lower().replace('en paris.cl', '').replace('paris', '')
            img_url = i.get('src')

            promo['nombre_promocion'] = unidecode(name)
            promo['tipo_oferta'] = tipo_oferta
            promo['posicion'] = position
            promo['url_img'] = img_url
            data.append(promo)
            position += 1
    df = pd.DataFrame(data)
    return df

## falabella scrapping
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
            promo['nombre_promocion'] = unidecode(name)
            promo['tipo_oferta'] = dict_sale_type[idx]
            promo['posicion'] = pos
            url = element.picture.find('source').get('srcset')
            formatted_url = ''.join(url.split('?disable')[0])
            promo['url_img'] = formatted_url
            data.append(promo)

    df = pd.DataFrame(data)
    return df


blacklist = ['falabella', 'sodimac', 'tottus', 'linio', 'cmr', 'nosotros', 'ecosistema', 'seguros', 'puntospesos', 'paris', 'paris.cl', 'lider', 'lider.cl',
             'walmart']
def flag_blacklist(row, blacklist=blacklist):
    row = str(row)
    tokens = re.findall(r"(?=("+'|'.join(blacklist)+r"))", row)
    if len(tokens) > 0:
      return 'flagged_as_blacklisted'
    else:
      return row


def main(argv, get_data=True):
    ''''testing: get promotions and discounts images from home site'''
    assert argv[1] in ['falabella', 'paris', 'lider-supermercado'], 'retails supported: falabella, paris and lider-supermercado as argv'

    if argv[1] == 'falabella':
        aux = 1
        url = 'https://www.falabella.com/falabella-cl'
        scroll_increment = 10
        scroll_delay = 1
        increment_speed_up = 300
        delay_speed_up = 1

    if argv[1] == 'paris':
        aux = 2
        url = 'https://paris.cl'
        scroll_increment = 15
        scroll_delay = 1
        increment_speed_up = 300
        delay_speed_up = 1

    if argv[1] == 'lider-supermercado':
        aux = 3
        url = 'https://www.lider.cl/supermercado/'
        scroll_increment = 5
        scroll_delay = 1.5
        increment_speed_up = 300
        delay_speed_up = 1

    # driver setup
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-notifications')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=binary_path)
    try:
        driver.get(url)
        time.sleep(2)

        scroll_all_website(driver, scroll_increment=scroll_increment, scroll_delay=scroll_delay,
                           increment_speed_up=increment_speed_up, delay_speed_up=delay_speed_up)

        # get code with lazyload-wrappers imgs loaded
        website_code = driver.page_source
        with open('webpage_source.txt', 'w', encoding='utf-8') as file:
            file.write(website_code)
        driver.quit()

        soup = BeautifulSoup(website_code, 'html.parser')
        #print(soup.prettify()) #for developing
        if get_data:
            if aux == 1:  # falabella
                top_banner = soup.find_all(has_specific_class_and_attribute_top_banner)
                second_banner = soup.find_all(has_specific_class_and_attribute_second_banner)
                grid = soup.find_all(has_specific_class_and_attribute_lower_grid)
                lowest_carousel = soup.find_all(has_specific_class_and_attribute_lowest_carousel)

                all_sections = [top_banner, second_banner, grid, lowest_carousel]
                df_imgs = get_df_with_imgs(all_sections)

            if aux == 2:  # paris
                top_banner = get_top_banner_promos_paris(soup, tipo_oferta='ofertas_principales', class_tag="flex-none rounded-lg relative")
                grid = get_grid_promos_paris(soup, tipo_oferta='grid_ofertas', class_tag="cursor-pointer relative")
                lowest_carousel = get_lowest_carousel_paris(soup, tipo_oferta='lo_ultimo')

                df_imgs = pd.concat([top_banner, grid, lowest_carousel])
                df_imgs = df_imgs.reset_index(drop=True)

            if aux == 3:
                top_banner = get_top_banner_promos_lider_supermarket(soup, tipo_oferta='ofertas_principales')
                grid = get_grid_promos_lider_supermarket(soup, tipo_oferta='grid_ofertas')
                lowest_offers = get_lowest_offers_lider_supermarket(soup, tipo_oferta='ofertas_final_pag')

                df_imgs = pd.concat([top_banner, grid, lowest_offers])
                df_imgs = df_imgs.reset_index(drop=True)


            df_imgs['nombre_promocion'] = df_imgs['nombre_promocion'].apply(lambda row: flag_blacklist(row))
            df_imgs = df_imgs[~df_imgs.nombre_promocion.isin(['flagged_as_blacklisted', ''])]  # filter out
            df_imgs = df_imgs.drop_duplicates().reset_index(drop=True)  # filter out
            df_imgs['datetime_checked'] = pd.to_datetime('today')
            print(df_imgs.head(10))
            df_imgs.to_csv(f'df_promos_retail_{argv[1]}.csv')

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(sys.argv)