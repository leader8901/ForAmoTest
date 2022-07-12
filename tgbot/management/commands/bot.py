from django.core.management.base import BaseCommand
import telebot
from telebot import apihelper, types  # Нужно для работы Proxy
from TestProject.settings import TOKEN, proxy
from tgbot.models import Profile, Message
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import requests
import json

bot = telebot.TeleBot(TOKEN)  # Передаём токен из файла env
apihelper.proxy = {'http': proxy}  # Передаём Proxy из файла env
print(bot.get_me())


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


# Тут работаем с командой start
@bot.message_handler(commands=['start'])
def welcome_start(message):
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(KeyboardButton('Отправить номер', request_contact=True))
    bot.send_message(message.chat.id, 'Привет, а дай номер 🖖🏻', reply_markup=btn)


@bot.message_handler(content_types=['contact'])
def contact(message):
    user_name = message.from_user.first_name
    phone = message.contact.phone_number
    if message.contact is not None:
        try:
            url = 'https://s1-nova.ru/app/private_test_python/'
            headers = {'Content-type': 'application/json',  # Определение типа данных
                       'Content-Encoding': 'utf-8'}
            data = '{"phone": "phone", "login": "user_name"}'

            bot.set_webhook(url, data, headers)

        except Exception as m:
            error_message = f'Произошла ошибка: {m}'
            print(error_message)
            raise m


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        try:
            bot.polling(none_stop=True, timeout=123, interval=2)
        except Exception as e:
            print(f'Error {e}')
