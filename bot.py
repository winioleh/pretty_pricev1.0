import telebot, os
from telebot import types
import requests
from pyzbar.pyzbar import decode
from PIL import Image
import sqlite3
import json
from test import tmp_geting_data
# from geting_data import get_a_comparison


TOKEN = '594661078:AAEYBoTw7zehPDkjtB6J572ly7IUvPq4m3s'
bot = telebot.TeleBot(TOKEN)
# conn = sqlite3.connect('users.db')
# c = conn.cursor()
# c.execute('DELETE FROM users')
# conn.commit()

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, '''Ви фотографуєте штрих-код товара \nі надсилаєте його нам, ми обробляємо його\nі видаємо вам пропозиції від магазинів \nз точними цінами.
    Також нам потрібні ваші дані,а саме номер мобільного та ваша місце \nзнаходження для визначення релевантних магазинів.''')


@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.send_message(message.chat.id, "EcoPrice - Розпочни економити вже зараз, я допоможу тобі знайти де купувати за найвигіднішою ціною.")


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone_number = message.contact.phone_number
    user_id = message.contact.user_id
    markup = types.ReplyKeyboardMarkup()
    add_user(user_id, phone_number)
    markup.add(types.KeyboardButton(text=u"Дати доступ до геолокації.", request_location=True))
    bot.send_message(message.chat.id, u"Нам потрібена ваша геолокація", reply_markup=markup)
    # bot.register_next_step_handler(message, get_location)
@bot.message_handler(content_types=['location'])
def handle_location(message):
    global location_massege
    location_massege = message
    longitude = message.location.longitude
    latitude = message.location.latitude
    choose_option(message)

        # bot.register_next_step_handler(message, choose_option)
    return (longitude, latitude)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # bot.send_message(message.chat.id, "Привіт ")
    markup = types.ReplyKeyboardMarkup()
    if user_in_db(message.from_user.id):
        markup.add(types.KeyboardButton(text=u"Дати доступ до геолокації.", request_location=True))
        bot.send_message(message.chat.id, u"Нам потрібена ваша геолокація", reply_markup=markup)
        # bot.register_next_step_handler(message, get_location)

    else:
        markup.add(types.KeyboardButton(text=u"Дати номер телефону.", request_contact=True))
        bot.send_message(message.chat.id, u"Нам потрібен ваш номер телефону", reply_markup=markup)
        # bot.register_next_step_handler(message, register_user_number)


def add_user(uid, phone_number):

    conn = sqlite3.connect('users.db')
    c = conn.cursor()


    c.execute('''SELECT phone_number FROM users WHERE uid=%s''' % str(uid))
    res = c.fetchall()

    if not len(res):
        c.execute('''INSERT INTO users VALUES (%s, %s)''' % (str(uid), phone_number))
    # else:
    conn.commit()

def show_user(uid):

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM users WHERE uid=%s''' % uid)
    res = c.fetchall()
    conn.commit()
    return res

def add_user_product(uid, barcode):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT INTO user_product VALUES (%s, %s)''' % (str(uid), barcode))
    conn.commit()

def get_products_with_user(uid):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM user_product WHERE user_id=%s''' % uid)
    res = c.fetchall()
    # print(res)
    conn.commit()
    return res

@bot.message_handler(content_types=['photo'])
def handle_file(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text=u"Повернутись до вибору опції."))
    if message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))

        with open('imgs/out.png', 'wb') as f:
            f.write(file.content)
            tmp = decode(Image.open("imgs/out.png"))
            if not tmp:
                bot.send_message(message.chat.id, u'Штрих код не знайдено, спробуйте ще раз')
            else:
                # print(tmp)
                decoded_barcode = str(tmp[0].data, 'utf-8')
                user_id = message.from_user.id
                add_user_product(user_id, decoded_barcode)
                # result = get_data_with_barcode(decoded_barcode)
                # result = search_price(decoded_barcode)

                # coord1, coord2 = get_location(location_massege)
                # print(coord1, coord2)
                # if result is None:
                #     bot.send_message(message.chat.id, 'No result')
                #     result = []
                # my_str = u"%s Ціни в мережах: \n"
                # for item in result:
                #     tmp = get_distance(coord1,coord2,str(item[0]))
                #     my_str += '%s: %s - %s\n ' % (item[0], item[1], tmp)
                # bot.send_message(message.chat.id, my_str)
                # bot.send_message(message.chat.id, u"Оберіть Опцію")

                result = tmp_geting_data(decoded_barcode)
                if result is None:
                    bot.send_message(message.chat.id, 'Товар не знайдено')
                else:
                    my_str = "Ціни в мережах: \n"
                # print(result)
                    for item in result:
                        my_str += '%s: %s\n' % (item['name'], item['price'])
                    bot.send_message(message.chat.id, my_str)
                    bot.send_message(message.chat.id, u"Оберіть Опцію")

    # elif message.text != '/start':
    #     bot.send_message(message.chat.id, u'Для визначення товару, нам потрібен штрих код, загрузіть фото штрихкоду.')
    #     bot.register_next_step_handler(message, handle_file)

def get_distance(u_latitude, u_longitude, shop_name):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT latitude, longitude FROM shop WHERE name='%s'" % shop_name)
    res = c.fetchall()
    s_latitude = res[0][0]
    s_longitude = res[0][1]
    api_key = 'AIzaSyBZkdLwnJT8z_0EcS5CYNwsDPWDikvzuqo'

    url = '''https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&key={4}'''.format(u_latitude,u_longitude,s_latitude,s_longitude,api_key)

    result = requests.get(url)

    return json.loads(result.text)['rows'][0]['elements'][0]['distance']['text']

def user_in_db(uid):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM users WHERE uid=%s''' % str(uid))
    res = c.fetchall()
    if len(res) > 0:
        return True
    else:
        return False


def get_data_with_barcode(barcode_str = '5000159461122'):
    conn = sqlite3.connect('test.db')

    c = conn.cursor()

    c.execute('''SELECT s.name, ps.price, p.name, p.barcode FROM product_shop ps
                 INNER JOIN shop as s ON ps.shop_id = s.id
                 INNER JOIN product as p ON ps.barcode = p.barcode
                 WHERE p.barcode = "%s" ORDER BY ps.price ''' % barcode_str)

    return c.fetchall()

def choose_option(message):
    print('choose_location_log')
    markup = types.ReplyKeyboardMarkup()

    markup.add(types.KeyboardButton(u'Порівняти ціну на товар'))
    bot.send_message(message.chat.id, u"Оберіть Опцію", reply_markup=markup)
    # bot.register_next_step_handler(message,check_option)

@bot.message_handler(func=lambda message: u'Порівняти ціну на товар' == message.text)
def compare_one_product(message):
    bot.send_message(message.chat.id, u"Загрузіть фото штрих коду")
    bot.register_next_step_handler(message, handle_file)



bot.polling()
