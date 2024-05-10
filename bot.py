import telebot
import buttons
import DB
from geopy import Nominatim

bot = telebot.TeleBot('7075188848:AAHSKp1o9EEDmuE9GZjeHX65wg_110n30iQ')
#  Объект локации
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0')

admin_id = 409251406

users = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Здравствуйте! Выберите язык!', reply_markup=buttons.btn_language())
    bot.register_next_step_handler(message, language_choice)


def language_choice(message):
    user_id = message.from_user.id
    if message.text == 'UZ':
        bot.send_message(user_id, f'Ассалому алейкум, {message.from_user.first_name}',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Напишите своё имя')
        bot.register_next_step_handler(message, user_check)
    elif message.text == 'RU':
        bot.send_message(user_id, f'Здравствуйте, {message.from_user.first_name}',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Напишите своё имя')
        bot.register_next_step_handler(message, user_check)


def user_check(message):
    user_id = message.from_user.id
    check = DB.check_user_db(user_id)
    if check:
        bot.send_message(user_id, 'Регистрация прошла успешно! Перейдите по ссылке, чтобы больше узнать о нас!',
                         reply_markup=buttons.btn_info())
    else:
        bot.send_message(user_id, 'Привет'  f'{message.from_user.first_name}, напишите своё имя для регистрации:',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Ваше имя успешно зарегистрированно! Теперь введите номер вашего телефона: ',
                     reply_markup=buttons.btn_number())
    bot.register_next_step_handler(message, get_number, user_name)


def get_number(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_number = message.contact.phone_number
        bot.send_message(user_id, 'Номер телефона успешно зарегистрирован! Теперь отправьте локацию: ',
                         reply_markup=buttons.btn_location())
        bot.register_next_step_handler(message, get_location, user_name, user_number)
    else:
        bot.send_message(user_id, 'Отправьте номер телефона через кнопку!', reply_markup=buttons.btn_number())
        bot.register_next_step_handler(message, get_number, user_name)


def get_location(message, user_name, user_number):
    user_id = message.from_user.id
    if message.location:
        user_location = geolocator.reverse(f'{message.location.latitude}, {message.location.longitude}')
        DB.register_db(user_name, user_id, user_number, str(user_location))
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Перейдите по ссылке, чтобы больше узнать о нас!', reply_markup=buttons.btn_info())

    else:
        bot.send_message(user_id, 'Отправьте локацию по кнопке: ', reply_markup=buttons.btn_location)
        bot.register_next_step_handler(message, get_location, user_name, user_number)


@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Добро пожаловать в админ-панель!',
                         reply_markup=buttons.admin_buttons())
        # Переход на этап выбора команды
        bot.register_next_step_handler(message, admin_choice)
    else:
        bot.send_message(message.from_user.id, 'Вы не админ!\n'
                                               'Нажмите /start')


def admin_choice(message):
    if message.text == 'Добавить услугу':
        bot.send_message(admin_id, 'Итак, давайте начнём! Введите название услуги',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_proced_title)
    elif message.text == 'Удалить услугу':
        procedure_check = DB.check_procedure_db()
        if procedure_check:
            bot.send_message(admin_id, 'Введите id процедуры', reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_procedure_to_del)
        else:
            bot.send_message(admin_id, 'Такой процедуры нет в базе!')
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Изменить цену услуги':
        procedure_check = DB.check_procedure_db()
        if procedure_check:
            bot.send_message(admin_id, 'Введите id процедуры', reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_procedure_to_edit_price)
        else:
            bot.send_message(admin_id, 'Такой процедуры нет в базе!')
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Перейти в меню':
        bot.send_message(admin_id, 'Прекрасно!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(admin_id, 'Добро пожаловать на наш сайт!', reply_markup=buttons.btn_info())
    else:
        bot.send_message(admin_id, 'Ошибка!', reply_markup=buttons.admin_buttons())
        bot.register_next_step_handler(message, admin_choice)


def get_proced_title(message):
    procedure_title = message.text
    bot.send_message(admin_id, 'Теперь напишите описание процедуры!')
    bot.register_next_step_handler(message, get_proced_description, procedure_title)


def get_proced_description(message, procedure_title):
    procedure_description = message.text
    bot.send_message(admin_id, 'Напишите цену процедуры')
    bot.register_next_step_handler(message, get_proced_price, procedure_title, procedure_description)


def get_proced_price(message, procedure_title, procedure_description):
    procedure_price = message.text
    bot.send_message(admin_id,
                     'Последний этап, зайдите на сайт https://postimages.org/ru/ и загрузите туда фото услуги.\n'
                     'Затем, отправьте мне прямую ссылку на фото!')
    bot.register_next_step_handler(message, get_proced_photo, procedure_title, procedure_description, procedure_price)


def get_proced_photo(message, procedure_title, procedure_description, procedure_price):
    procedure_photo = message.text
    bot.send_message(admin_id, 'Укажите категорию процедуры')
    bot.register_next_step_handler(message, get_proced_category, procedure_title, procedure_description,
                                   procedure_price, procedure_photo)


def get_proced_category(message, procedure_title, procedure_description, procedure_price, procedure_photo):
    procedure_category = message.text
    DB.add_procedure_db(procedure_title, procedure_description, procedure_price, procedure_photo, procedure_category)
    bot.send_message(admin_id, 'Готово! Хотите чего-то ещё?', reply_markup=buttons.admin_buttons())
    bot.register_next_step_handler(message, admin_choice)


def get_procedure_to_del(message):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Пишите только целые числа!')
        bot.register_next_step_handler(message, get_procedure_to_del)
    else:
        procedure_id = int(message.text)
        DB.delete_procedure_db(procedure_id)
        bot.send_message(admin_id, 'Процедура успешно удалена!', reply_markup=buttons.admin_buttons())
        bot.register_next_step_handler(message, admin_choice)


def get_procedure_to_edit_price(message):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Пишите только целые числа!')
        bot.register_next_step_handler(message, get_procedure_to_edit_price)
    else:
        procedure_id = int(message.text)
        bot.send_message(admin_id, 'Напишите новую цену услуги')
        bot.register_next_step_handler(message, edit_price, procedure_id)


def edit_price(message, procedure_id):
    new_price = message.text
    DB.change_procedure_price_db(procedure_id, new_price)
    bot.send_message(admin_id, 'Цена процедуры успешно изменена!', reply_markup=buttons.admin_buttons())
    bot.register_next_step_handler(message, admin_choice)


bot.polling(none_stop=True)
