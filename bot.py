import telebot, os
from telebot import types
# from telebot import
from settings import TOKEN
import requests
# from pyTelegramBotAPI import users
from pyzbar.pyzbar import decode
from PIL import Image
import sqlite3
import json
# from reg_user import add_user, add_user_product

bot = telebot.TeleBot(TOKEN)

def get_distance(u_latitude, u_longitude, shop_name):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT latitude, longitude FROM shop WHERE name='%s'" % shop_name)
    res = c.fetchall()
    # print(res[0])
    s_latitude = res[0][0]
    s_longitude = res[0][1]
    print(u_latitude)
    print(u_longitude)
    print('\n')
    print(s_latitude)
    print(s_longitude)
    api_key = 'AIzaSyBZkdLwnJT8z_0EcS5CYNwsDPWDikvzuqo'
    # url = '''https://maps.googleapis.com/maps/api/distancematrix/json?origins=48.291342,25.936575&
    #                             destinations=48.291983,25.940850&key=%s''' % api_key

    url = '''https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&key={4}'''.format(u_latitude,u_longitude,s_latitude,s_longitude,api_key)

    result = requests.get(url)
    # print(json.loads(result.text)['rows'][0]['elements'][0]['distance']['text'])
    # print(json.loads(result.text))
    # print(url)
    # return 20
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

    try:
        markup = types.ReplyKeyboardMarkup()
        # print(message.location.longitude)
        longitude = message.location.longitude
        latitude = message.location.latitude

        markup.add(types.KeyboardButton('Порівняти ціну на товар'))
        bot.send_message(message.chat.id, "Оберіть Опцію", reply_markup=markup)


    # print((longitude, latitude))

        return (longitude, latitude)
    except:
    #     print("Cant get coords")
        return (25.936889,48.270142)

# @bot.message_handler(content_types=['location'])
# def ttt(message):
#     print("wini")
#     bot.send_message(message.chat.id, "Q!!!!!!!!!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    # markup.add(types.KeyboardButton(text="Дати номер телефону.", request_contact=True))
    if user_in_db(message.from_user.id):
        markup.add(types.KeyboardButton(text="Дати доступ до гуолокації.", request_location=True))
        bot.send_message(message.chat.id, "Нам потрібена ваша геолокація", reply_markup=markup)
        bot.register_next_step_handler(message, get_location)

        # bot.send_message(message.chat.id, "Оберіть Опцію")

    else:
        markup.add(types.KeyboardButton(text="Дати номер телефону.", request_contact=True))
        bot.send_message(message.chat.id, "Нам потрібен ваш номер телефону",reply_markup=markup)
        bot.register_next_step_handler(message, register_user_number)
    # markup.add(types.KeyboardButton('Порівняти ціну на товар'))
    # markup.add(types.KeyboardButton('Нам потрібер ваш номер телефону.'))
    # bot.send_message(message.chat.id, "Нам потрібер ваш номер телефону.", reply_markup=markup)
    # markup.add(types.KeyboardButton('Порівняти ціну на корзину'))
    #
    # bot.send_message(message.chat.id, "Оберіть Опцію.", reply_markup=markup)

# @bot.message_handler(types=['text'])


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
    # print(res)
    conn.commit()
    return res

def register_user_number(message):

    phone_number = message.contact.phone_number
    user_id = message.contact.user_id
    # print(user_id)
    # print(type(phone_number))
    add_user(user_id, phone_number)
    # a = show_user(391727814)
    # print(a)
    markup=types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text="Дати доступ до гуолокації.", request_location=True))
    bot.send_message(message.chat.id, "Нам потрібена ваша геолокація", reply_markup=markup)
    bot.register_next_step_handler(message, get_location)






@bot.message_handler(func=lambda message: 'Порівняти ціну на товар' == message.text)
def compare_one_product(message):
    bot.send_message(message.chat.id, "Загрузіть фото штрих коду")
    bot.register_next_step_handler(message, handle_file)
    # file_get_contents("https://api.telegram.org/bot$apiToken/sendMessage?".http_build_query($data) );
    # bot.send_message(message.chat.id, )
#
#
# @bot.message_handler(func=lambda message: 'Нам потрібер ваш номер телефону.' == message.text)
# def compare_one_product(message):
#     # user_info = users.getFullUser(message.from_user.id)
#     print(userStep)
#     # bot.send_message(message.chat.id,  message.contact.phone_number)
#     bot.register_next_step_handler(message, handle_file)
#     # file_get_contents("https://api.telegram.org/bot$apiToken/sendMessage?".http_build_query($data) );
#     # bot.send_message(message.chat.id, )


def add_user_product(uid, barcode):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT INTO user_product VALUES (%s, %s)''' % (str(uid), barcode))
    conn.commit()
    # result = c.fetchall()
    # print(result)


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
                bot.send_message(message.chat.id, 'Штрих код не знайдено, спробуйте ще раз')
            else:
                # print(tmp)
                decoded_barcode = str(tmp[0].data, 'utf-8')
                # print(decoded_barcode)
                # print(message.from_user.id)
                user_id = message.from_user.id
                add_user_product(user_id, decoded_barcode)
                # print(get_products_with_user(user_id))
                result = get_data_with_barcode(decoded_barcode)
                coord1, coord2 = get_location(message)
                # print(coord1)
                # print(coord2)
                if result is None:
                    bot.send_message(message.chat.id, 'No result')
                    result = []
                my_str = "%s Ціни в мережах: \n" % result[0][2]
                # print(result)
                for item in result:
                    tmp = get_distance(coord1,coord2,str(item[0]))
                    # print
                    my_str += '%s: %s - %s\n ' % (item[0], item[1], tmp)
                bot.send_message(message.chat.id, my_str)
                bot.send_message(message.chat.id, "Оберіть Опцію")

bot.polling()

#
# @bot.message_handler(func=lambda message: 'Порівняти ціну на корзину' == message.text)
# def compare_basket(message):
#     markup = types.ReplyKeyboardMarkup()
#     markup.row('Завантажити')
#     markup.row('Стоп')
#     bot.send_message(message.chat.id, "Загрузіть фото штрих коду", reply_markup=markup)
#     bot.register_next_step_handler(message, handle_next_photo_uploading)
#     # file_get_contents("https://api.telegram.org/bot$apiToken/sendMessage?".http_build_query($data) );
#     # bot.send_message()


# def handle_next_photo_uploading(message):
#
#     tmp_str = str(message.chat.id)
#     if not os.path.isdir(tmp_str):
#         os.makedirs(tmp_str)
#     if message.text and message.text.lower() == 'стоп':
#         basket = Basket(message.chat.id)
#         response = basket.response
#         basket.clear()
#         # send_welcome('/start')
#         bot.send_message(message.chat.id, response)
#
#         return
#
#     if message.photo:
#         file_id = message.photo[-1].file_id
#
#         file_info = bot.get_file(file_id)
#         file_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)
#         file = requests.get(file_url)
#
#         last_n = max(list(map(lambda x: int(x.split('out')[1].split('.')[0]), os.listdir(tmp_str))) or [0])
#         # print(map(lambda x: int(x.split('.')[1]), os.listdir(tmp_str)))
#
#         with open('%s/out%s.png' % (message.chat.id, last_n + 1), 'wb') as f:
#             f.write(file.content)
#
#
#
#     markup = types.ReplyKeyboardMarkup()
#     bot.send_message(message.chat.id, "Загрузіть фото штрих коду", reply_markup=markup)
#     bot.register_next_step_handler(message, handle_next_photo_uploading)


# @bot.message_handler(func=lambda message: 'Оборот по магазинам' == message.text)
# def turnover_by_shops(message):


