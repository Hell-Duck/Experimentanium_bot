import telebot
from telebot import types
from info import *


try:
    with open('token.txt', 'r') as file:
        TOKEN = file.read().strip()

    if not TOKEN:
        raise ValueError("Файл token.txt пустой")

    bot = telebot.TeleBot(TOKEN)

except FileNotFoundError:
    print("Ошибка: файл token.txt не найден")
    exit()
except Exception as e:
    print(f"Ошибка при чтении токена: {e}")
    exit()


@bot.message_handler(commands = ['start'])
def menu(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn_start = types.KeyboardButton('Меню')
        markup.row(btn_start)

        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!', reply_markup=markup)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


@bot.message_handler(func=lambda message: message.text == 'Меню')
def main(message):
    markup = types.InlineKeyboardMarkup()

    btn_site = types.InlineKeyboardButton('Перейти на сайт', url='https://www.experimentanium.ru/')
    btn_contact = types.InlineKeyboardButton('Контакты', callback_data = 'get_contact')
    btn_work_time = types.InlineKeyboardButton('Время работы', callback_data = 'get_work_time')
    btn_useful_links = types.InlineKeyboardButton('Полезные ссылки', callback_data = 'get_links')
    btn_birthday = types.InlineKeyboardButton('О проведении дня рождения', callback_data = 'get_birthday')
    btn_excursions = types.InlineKeyboardButton('Экскурсии', callback_data = 'get_excursions')
    btn_address = types.InlineKeyboardButton('Адрес', callback_data = 'get_address')
    btn_show = types.InlineKeyboardButton('Шоу, мастер-классы, квизы', url='https://www.experimentanium.ru/show/')
    btn_price = types.InlineKeyboardButton('Цены на входные билеты', url='https://experimentanium.ru/prices/')
    markup.row(btn_site, btn_contact)
    markup.row(btn_work_time, btn_address)
    markup.row(btn_excursions, btn_useful_links)
    markup.row(btn_price)
    markup.row(btn_show)
    markup.row(btn_birthday)


    bot.send_message(message.chat.id, 'Нажмите на кнопку для получения информации', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    responses = {
        'get_contact': (data, "HTML"),
        'get_work_time': ('Мы работаем каждый день с 9:30 до 20:00, кроме 31.12 и 01.01', None),
        'get_links': (links, "HTML"),
        'get_excursions': (excursions, "HTML"),
        'get_birthday': (birthday, "HTML"),
        'get_address': (address, "HTML"),
    }

    if callback.data in responses:
        text, parse_mode = responses[callback.data]

        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('Вернуться в меню', callback_data='back_to_menu')
        markup.row(btn_back)

        bot.send_message(callback.message.chat.id, text,
                         parse_mode=parse_mode,
                         reply_markup=markup)

    elif callback.data == 'back_to_menu':
        main(callback.message)

bot.polling(none_stop=True, skip_pending=True)