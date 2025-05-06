

import telebot
import random
import string


TOKEN = '8137093677:AAFk7pvkeH819sk5nLPLkanJD774U6WHYCg'


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
   bot.reply_to(message, "Привет! Я бот для генерации паролей.\nНапиши длину пароля, например: 12")


@bot.message_handler(func=lambda message: message.text.isdigit())
def generate_password(message):
   length = int(message.text)
   if length < 4:
      bot.reply_to(message, "Слишком короткий пароль. Введи число больше 3.")
      return
   characters = string.ascii_letters + string.digits + string.punctuation
   password = ''.join(random.choice(characters) for _ in range(length))
   bot.reply_to(message, f"Вот твой пароль:\n{password}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
   bot.reply_to(message, "Пожалуйста, введи число — длину пароля.")


print("Бот запущен!")
bot.polling()