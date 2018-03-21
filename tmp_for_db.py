import sqlite3
conn = sqlite3.connect('test.db')

c = conn.cursor()

# c.execute('''CREATE TABLE product
#              (barcode text, name text)''')
#
# c.execute('''CREATE TABLE shop
#              (id int, name text)''')
#
# c.execute('''CREATE TABLE product_shop
#              (barcode text, shop_id int, price real)''')


# Insert a row of data


names = ['Шок. Корона 90г', 'Майонез Торчин Європейський', 'Садочок Яблуко-Виноград Нектар', 'Снікерс 50г',
         'Малоко Молокія 2.5', 'Горілка Гріндей органік 0.5', 'Вино Віла Крім чер. н.сол', 'Кока Кола 2л',
         'Моршинська Сильногазована1.5', 'Пиво Львівське 1715 0.5', 'Чіпси Люкс 133г','Торчин Кетчуп Лагідний',
         'Олія Олейна']
barcodes = ["7622210354419", "4820001316001", "4823063107327", "5000159461122", "4820045701665", "4820073561774",
            "4820024225021", "5449000009067", "4820017000055", "4820000455732", "7622210176196", "4820001313581",
            "4820001116304"]

product_dict = {key:value for key, value in zip(barcodes, names)}
# print(product_dict)
# for key,value in product_dict.items():
#     c.execute("INSERT INTO product VALUES ('%s','%s')" % (key, value))
# c.execute('SELECT * FROM product')
# print(c.fetchall())
# conn.commit()

shops = {'Норма': 1, 'Нива': 2, 'Сільпо': 3, 'Тайстра': 4, 'Колос': 5}

# for key, value in shops.items():
#     c.execute("INSERT INTO shop VALUES ('%s','%s')" % (value, key))
#
# c.execute('SELECT * FROM shop')
# print(c.fetchall())
# conn.commit()

# c.execute("INSERT INTO product_shop VALUES ('4820001116304', 1 ,'30.99')")
# c.execute("INSERT INTO product_shop VALUES ('4820001116304', 2 ,'32.50')")
# c.execute("INSERT INTO product_shop VALUES ('4820001116304', 3 ,'37.97')")
# c.execute("INSERT INTO product_shop VALUES ('4820001116304', 4 ,'32.47')")
# c.execute("INSERT INTO product_shop VALUES ('4820001116304', 5 ,'35.50')")

c.execute('''SELECT s.name, ps.price, p.name, p.barcode FROM product_shop ps
             INNER JOIN shop as s ON ps.shop_id = s.id
             INNER JOIN product as p ON ps.barcode = p.barcode
             WHERE p.barcode = "7622210176196" ''')


# c.execute("SELECT * FROM product_shop")
# conn.commit()
#
res = c.fetchall()
print(res)
# print(len(res))
# for i in res:
#     print(i)
conn.close()
