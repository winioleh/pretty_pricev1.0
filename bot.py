import telebot, os
from telebot import types
from settings import TOKEN
import requests
from pyzbar.pyzbar import decode
from PIL import Image
import sqlite3

bot = telebot.TeleBot(TOKEN)


def get_data_with_barcode(barcode_str = '5000159461122'):
    conn = sqlite3.connect('test.db')

    c = conn.cursor()

    c.execute('''SELECT s.name, ps.price, p.name, p.barcode FROM product_shop ps
                 INNER JOIN shop as s ON ps.shop_id = s.id
                 INNER JOIN product as p ON ps.barcode = p.barcode
                 WHERE p.barcode = "%s" ORDER BY ps.price ''' % barcode_str)

    return c.fetchall()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Порівняти ціну на товар'))
    # markup.add(types.KeyboardButton('Порівняти ціну на корзину'))
    # markup.add(types.KeyboardButton('Оборот по магазинам'))
    bot.send_message(message.chat.id, "Оберіть Опцію.", reply_markup=markup)


@bot.message_handler(func=lambda message: 'Порівняти ціну на товар' == message.text)
def compare_one_product(message):
    bot.send_message(message.chat.id, "Загрузіть фото штрих коду")
    bot.register_next_step_handler(message, handle_file)
    # file_get_contents("https://api.telegram.org/bot$apiToken/sendMessage?".http_build_query($data) );
    # bot.send_message(message.chat.id, )



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

                result = get_data_with_barcode(decoded_barcode)
                if result is None:
                    bot.send_message(message.chat.id, 'No result')
                    result = []
                my_str = "%s Ціни в мережах: \n" % result[0][2]
                # print(result)
                for item in result:
                    my_str += '%s: %s\n' % (item[0], item[1])
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


