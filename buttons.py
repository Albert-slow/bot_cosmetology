from telebot import types


def btn_language():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_ru = types.KeyboardButton(text='RU')
    btn_uz = types.KeyboardButton(text='UZ')
    kb.add(btn_ru, btn_uz)
    return kb


def btn_number():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    number = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(number)
    return kb


def btn_location():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(location)
    return kb


def btn_info():
        kb = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text='Ссылка на наш сайт:', url='https://github.com/Albert-slow'
                                                                                '/bot48_test')
        kb.add(url_button)
        return kb


def admin_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_service = types.KeyboardButton('Добавить услугу')
    del_service = types.KeyboardButton('Удалить услугу')
    edit_price = types.KeyboardButton('Изменить цену услуги')
    to_menu = types.KeyboardButton('Перейти в меню')
    kb.add(add_service, edit_price, del_service)
    kb.row(to_menu)
    return kb
