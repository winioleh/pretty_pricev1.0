from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException

# 4820001313581  рафаелло
# 4820001313581 кетчуп
# 4820000455732  львівське пиво
# 4820017000055 моршинська
# 4820073561774 грін дей
# 4820045701665 молоко


# def search_price(barcode=4820017000055):
#     driver = webdriver.PhantomJS()
#     classNameForNovusAndFozzy = 'one-product-price'
#     selectorForAushanAnaMetro = '.product-card-info > div:nth-child(1) > strong:nth-child(1)'
#     metroUrl = 'https://metro.zakaz.ua/ru/?q=0'
#     aushnUrl = 'https://auchan.zakaz.ua/ru/?q=0'
#     fozzyUrl = 'https://fozzy.zakaz.ua/ru/?q=0'
#     novusUrl = 'https://novus.zakaz.ua/ru/?q=0'
#     tmp_dict = {}
#     shops = {'Metro':metroUrl, 'Aushan':aushnUrl, "Novus":novusUrl, 'Fozzy':fozzyUrl}
#     for shop_name, shop_url in shops.items():
#         # print(shop_name, shop_url)
#         if shop_name == 'Metro' or shop_name == 'Aushan':
#             driver.get(shop_url + str(barcode))
#             try:
#                 # driver.find_element_by_css_selector(selectorForAushanAnaMetro):
#                 pageBody = driver.find_element_by_css_selector(selectorForAushanAnaMetro).get_attribute("outerHTML")
#                 soup = BeautifulSoup(pageBody, "html.parser")
#                 product_price = soup.find('strong').string
#                 tmp_dict[shop_name] = product_price
#             except NoSuchElementException:
#                 tmp_dict[shop_name] = 'немає в наявності'
#         else:
#             driver.get(shop_url + str(barcode))
#             # if driver.find_element(selectorForNovusAndFozzy):
#             try:
#                 pageBody = driver.find_element_by_class_name(classNameForNovusAndFozzy).get_attribute("outerHTML")
#                 soup = BeautifulSoup(pageBody, "html.parser")
#                 span_product_grivna_price = soup.find('span', class_='grivna price').string
#                 span_product_kopeiki_price = soup.find('span', class_='kopeiki').string
#                 product_price = str(span_product_grivna_price) + '.' + str(span_product_kopeiki_price)
#                 tmp_dict[shop_name] = product_price
#             except NoSuchWindowException:
#             # except Exception as e:
#                 # print(e)
#                 tmp_dict[shop_name] = 'немає в наявності'
#     print(tmp_dict)
#     driver.quit()
#
# if __name__ == "__main__":
#     search_price(4820000455732)
    # get_data_with_barcode()

import urllib.request
from bs4 import BeautifulSoup
import csv

product_bar_code = '4820045701665'
BASE_URL = 'https://fozzy.zakaz.ua/ru/?q=0' + product_bar_code


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html,"html.parser")
    div_product = soup.find('button', class_='btn btn-mini product-add-to-cart-button')
    span_product_price = div_product.find('span', class_='one-product-price')
    span_product_grivna_price = span_product_price.find('span', class_='grivna price').string
    span_product_kopeiki_price = span_product_price.find('span', class_='kopeiki').string
    print(span_product_grivna_price+'.'+span_product_kopeiki_price)

parse(get_html(BASE_URL))