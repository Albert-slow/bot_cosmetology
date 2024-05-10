import sqlite3

connection = sqlite3.connect('bot_users.db', check_same_thread=False)
sql = connection.cursor()

# Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, number TEXT, location TEXT);')

# Создание таблицы услуг
sql.execute('CREATE TABLE IF NOT EXISTS procedures(procedure_id INTEGER, procedure_title TEXT,'
            'procedure_description TEXT, procedure_price TEXT, procedure_image TEXT, procedure_category TEXT);')

# Создание таблицы корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart(id INTEGER, user_phone_number, user_proced_title TEXT, total_price REAL);')


def check_user_db(user_id):
    check = sql.execute('SELECT * FROM users WHERE id=?;', (user_id,))
    if check.fetchone():
        return True
    else:
        return False


def register_db(name, id, number, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (name, id, number, location))
    connection.commit()


## Методы для процедур
# Сторона админа
def add_procedure_db(procedure_title, procedure_description, procedure_price, procedure_image, procedure_category):
    sql.execute('INSERT INTO procedures(procedure_title, procedure_description, procedure_price,'
                'procedure_image, procedure_category) VALUES(?, ?, ?, ?, ?);',
                (procedure_title, procedure_description, procedure_price, procedure_image, procedure_category))
    connection.commit()


def delete_procedure_db(procedure_id):
    sql.execute('DELETE FROM procedures WHERE procedure_id=?;', (procedure_id,))
    connection.commit()


def change_procedure_price_db(procedure_id, new_price):
    sql.execute('UPDATE procedures SET procedure_price=? WHERE procedure_id=?;', (new_price, procedure_id))
    connection.commit()


def check_procedure_db():
    if sql.execute('SELECT * FROM procedures;').fetchall():
        return True
    else:
        return False


# Сторона пользователя
def get_procedures_db():
    return sql.execute('SELECT procedure_id, procedure_title FROM procedures;').fetchall()


def get_exact_procedure_db(procedure_id):
    return sql.execute('SELECT procedure_title, procedure_description, procedure_price, procedure_image,'
                       'procedure_category FROM procedures WHERE procedure_id=?;', (procedure_id,)).fetchone()


# Добавление процедуры в корзину
def add_proced_to_cart_db(user_id, user_phone_number, user_proced_title, total_price):
    sql.execute('INSERT INTO cart VALUES(?, ?, ?);', (user_id, user_phone_number, user_proced_title, total_price))
    connection.commit()
