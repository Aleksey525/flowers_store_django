import telebot
from django.conf import settings


bot = telebot.TeleBot(settings.BOT_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет!')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)