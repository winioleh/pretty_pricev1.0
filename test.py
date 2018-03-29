import urllib
from bs4 import BeautifulSoup
import re
import requests
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException

def tmp_geting_data(product_bar_code = '7622210176196'):
    fozzyUrl = 'https://fozzy.zakaz.ua/ru/?q=0'
    novusUrl = 'https://novus.zakaz.ua/ru/?q=0'
    tmp_list = []
    shops = {"Novus": novusUrl, 'Fozzy': fozzyUrl}

    for shop_name, shop_url in shops.items():
        tmp_dict = {}
        try:
            response = urllib.request.urlopen(shop_url + str(product_bar_code))
            soup = BeautifulSoup(response, "html.parser")
            div_product = soup.find('button', class_='btn btn-mini product-add-to-cart-button')
            span_product_price = div_product.find('span', class_='one-product-price')
            span_product_grivna_price = span_product_price.find('span', class_='grivna price').string
            span_product_kopeiki_price = span_product_price.find('span', class_='kopeiki').string
            product_price = span_product_grivna_price + '.' + span_product_kopeiki_price

            tmp_dict['name'] = shop_name
            tmp_dict['price'] = product_price
        except:
            tmp_dict['name'] = shop_name
            tmp_dict['price'] = 'немає в наявності'
        # except NoSuchElementException:
        #     pass
        tmp_list.append(tmp_dict)
    # print(tmp_list)
    return tmp_list

# tmp_geting_data('4823063104227')