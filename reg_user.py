import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# c.execute('''CREATE TABLE users
#              (uid text, phone_number text)''')

# c.execute('''CREATE TABLE user_product
#              (user_id text, barcode text)''')



def add_user(uid, phone_number):
    c.execute('''SELECT phone_number FROM users WHERE uid=%s''' % str(uid))
    res = c.fetchall()

    if not len(res):
        c.execute('''INSERT INTO users VALUES (%s, %s)''' % (str(uid), phone_number))
    # else:
    conn.commit()


def show_user(uid):

    c.execute('''SELECT phone_number FROM users WHERE uid=%s''' % uid)
    res = c.fetchall()
    # print(res)
    conn.commit()
    return res

def add_user_product(uid, barcode):
    c.execute('''INSERT INTO user_product VALUES (%s, %s)''' % (str(uid), barcode))
    conn.commit()
    # result = c.fetchall()
    # print(result)


def get_products_with_user(uid):
    c.execute('''SELECT * FROM user_product WHERE user_id=%s''' % uid)
    res = c.fetchall()
    print(res)
    conn.commit()
    return res

#
# c.execute('''DELETE  FROM user_product''' )
# c.execute('''DELETE  FROM users''' )
# conn.commit()

# add_user(32131, "+380935032691")
#
# show_user(32131)
# add_user_product(32131, "935032691")
# add_user_product(32131, "935032692")
# add_user_product(32131, "935032693")
# add_user_product(32131, "935032694")
# add_user_product(32131, "935032694")
#
# get_products_with_user(32131)
# 48.291342, 25.936575
c.execute('DELETE FROM users')
conn.commit()

import requests, json

api_key = 'AIzaSyBZkdLwnJT8z_0EcS5CYNwsDPWDikvzuqo'
url = '''https://maps.googleapis.com/maps/api/distancematrix/json?origins=25.936889,48.270142&destinations=48.296699,25.898772&key=%s''' % api_key
      # 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=25.936889,48.270142&destinations=48.296699,25.898772&key=AIzaSyBZkdLwnJT8z_0EcS5CYNwsDPWDikvzuqo'
result = requests.get(url)
print(json.loads(result.text)['rows'][0]['elements'][0]['distance']['text'])
