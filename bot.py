import telebot, os
from telebot import types
import requests
from pyzbar.pyzbar import decode
from PIL import Image
import sqlite3
import json

TOKEN = '535846211:AAGZo7FNi0wRlLNBTWXRVxHYmyNjrkHOTVA'
bot = telebot.TeleBot(TOKEN)


def get_distance(u_latitude, u_longitude, shop_name):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT latitude, longitude FROM shop WHERE name='%s'" % shop_name)
    res = c.fetchall()
    s_latitude = res[0][0]
    s_longitude = res[0][1]
    print(u_latitude)
    print(u_longitude)
    print('\n')
    print(s_latitude)
    print(s_longitude)
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
def get_location(message):

    # try:
    markup = types.ReplyKeyboardMarkup()
    longitude = message.location.longitude
    latitude = message.location.latitude
    global location_massege
    location_massege = message
    markup.add(types.KeyboardButton(u'Порівняти ціну на товар'))
    bot.send_message(message.chat.id, u"Оберіть Опцію", reply_markup=markup)


    print(longitude, latitude)
    return (longitude, latitude)
    # except:
        # return (25.936889,48.270142)
        # pass
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    if user_in_db(message.from_user.id):
        markup.add(types.KeyboardButton(text=u"Дати доступ до гуолокації.", request_location=True))
        bot.send_message(message.chat.id, u"Нам потрібена ваша геолокація", reply_markup=markup)
        bot.register_next_step_handler(message, get_location)


    else:
        markup.add(types.KeyboardButton(text=u"Дати номер телефону.", request_contact=True))
        bot.send_message(message.chat.id, u"Нам потрібен ваш номер телефону",reply_markup=markup)
        bot.register_next_step_handler(message, register_user_number)

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

def register_user_number(message):

    phone_number = message.contact.phone_number
    user_id = message.contact.user_id

    add_user(user_id, phone_number)
    markup=types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text=u"Дати доступ до гуолокації.", request_location=True))
    bot.send_message(message.chat.id, u"Нам потрібена ваша геолокація", reply_markup=markup)
    bot.register_next_step_handler(message, get_location)






@bot.message_handler(func=lambda message: u'Порівняти ціну на товар' == message.text)
def compare_one_product(message):
    bot.send_message(message.chat.id, u"Загрузіть фото штрих коду")
    bot.register_next_step_handler(message, handle_file)


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


def handle_file(message):
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
                result = get_data_with_barcode(decoded_barcode)

                coord1, coord2 = get_location(location_massege)
                print(coord1, coord2)
                if result is None:
                    bot.send_message(message.chat.id, 'No result')
                    result = []
                my_str = u"%s Ціни в мережах: \n" % result[0][2]
                for item in result:
                    tmp = get_distance(coord1,coord2,str(item[0]))
                    my_str += '%s: %s - %s\n ' % (item[0], item[1], tmp)
                bot.send_message(message.chat.id, my_str)
                bot.send_message(message.chat.id, u"Оберіть Опцію")

bot.polling()
