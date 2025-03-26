import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
import requests
import time
import sqlite3


bot = telebot.TeleBot('7780668347:AAFTwSbXzNg02naVu_g2x-k2GiPiYPVlOng')
api_key = '17697edb22cd6287f4a12ccb3e497513'


def get_city_info(name):
   conn = sqlite3.connect('cities.db')
   cursor = conn.cursor()
   cursor.execute('SELECT description, image_url FROM cities WHERE name = ?', (name,))
   result = cursor.fetchone()
   conn.close()
   return result


def get_city_list():
   conn = sqlite3.connect('cities.db')
   cursor = conn.cursor()
   cursor.execute('SELECT name FROM cities')
   cities = [city[0] for city in cursor.fetchall()]
   conn.close()
   return cities

cities = get_city_list()


@bot.message_handler(commands=['help'])
def help(message):
   bot.send_message(message.chat.id, 
                     "<b>Мои команды:</b>\n"
                     "/start — начать общение с ботом\n"
                     "/help — получить справку о боте\n"
                     "/about — узнать информацию о разработчике\n"
                     "/stop — завершить общение с ботом", parse_mode='html')

@bot.message_handler(commands=['about'])
def about(message):
   bot.send_message(message.chat.id, 
                     "Этот бот был создан в рамках проекта по изучению Python и Telegram API.\n"
                     "Разработчик: <em><b>yerazz</b></em>", parse_mode='html')

@bot.message_handler(commands=['stop'])
def stop(message):

   # chat_id = message.chat.id
   # for i in range(message.message_id - 20, message.message_id + 1):
   #    try:
   #       bot.delete_message(chat_id, i)
   #    except Exception as e:
   #       print(f"Не удалось удалить сообщение {i}: {e}")

   bot.send_message(message.chat.id, "До свидания! Бот остановлен и больше не реагирует на сообщения.")
   os._exit(0)

@bot.message_handler(commands=['start'])
def start(message):

   command_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   command_markup.row('/start', '/stop')
   command_markup.row('/help', '/about')

   bot.send_message(message.chat.id, 
                     f"Привет, {message.from_user.first_name}! 👋\n"
                     "Я - твой персональный гид по Казахстану! 🇰🇿\n"
                     "Могу показать тебе интересные места, рассказать факты и подсказать погоду. 🌍✨", reply_markup=command_markup)

   inline_markup = types.InlineKeyboardMarkup()
   btn1 = types.InlineKeyboardButton('Выбрать город', callback_data='select_city')
   btn2 = types.InlineKeyboardButton('Ввести название', callback_data='input_city')
   inline_markup.row(btn1, btn2)

   bot.send_message(message.chat.id, "Для начала выбери действие:",  reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(callback):
   if callback.data == 'select_city':
      markup = types.InlineKeyboardMarkup()
      for city in cities:
         markup.add(types.InlineKeyboardButton(city, callback_data=city))
      bot.send_message(callback.message.chat.id, "Выбери город из списка:", reply_markup=markup)

   elif callback.data == 'input_city':
      msg = bot.send_message(callback.message.chat.id, "Введите название города:")
      bot.register_next_step_handler(msg, process_city_input)

   elif callback.data in cities:
      city = callback.data
      city_info = get_city_info(city)
      if city_info:
         description, image_url = city_info
         bot.send_photo(callback.message.chat.id, open(image_url, 'rb'))
         bot.send_message(callback.message.chat.id, f"🏙️ *{city}*\n\n{description}", parse_mode='Markdown')
      else:
         bot.send_message(callback.message.chat.id, "❗ Информация о городе не найдена.")

def process_city_input(message):
   city_name = message.text
   city_info = get_city_info(city_name)
   if city_info:
      description, image_url = city_info
      bot.send_photo(message.chat.id, open(image_url, 'rb'))
      bot.send_message(message.chat.id, f"🏙️ {city_name}\n\n{description}", parse_mode='Markdown')
   else:
      bot.send_message(message.chat.id, "❗ Город не найден. Попробуйте снова.")

bot.polling(none_stop=True)