import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
import requests
import time
import sqlite3
from bs4 import BeautifulSoup


bot = telebot.TeleBot('7780668347:AAFTwSbXzNg02naVu_g2x-k2GiPiYPVlOng')


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



api_key = '17697edb22cd6287f4a12ccb3e497513'
weather_cache = {}
CACHE_TIMEOUT = 600  # 10 минут

def get_weather(city):
      current_time = time.time()
      if city in weather_cache and current_time - weather_cache[city]['time'] < CACHE_TIMEOUT:
         return weather_cache[city]['data']

      url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
      response = requests.get(url).json()
      if response.get("main"):
         weather_desc = response['weather'][0]['description']
         temp = response["main"]["temp"]
         wind = response["wind"]["speed"]
         humidity = response["main"]["humidity"]
         pressure = response["main"]["pressure"]
         cloudiness = response["clouds"]["all"]

         weather_data = (
            f"{weather_desc.capitalize()}\n"
            f"🌡️ Температура: {temp}°C\n"
            f"💨 Ветер: {wind} м/с\n"
            f"💧 Влажность: {humidity}%\n"
            f"🔽 Давление: {pressure} мм рт. ст.\n"
            f"☁️ Облачность: {cloudiness}%"
         )
         weather_cache[city] = {'data': weather_data, 'time': current_time}
         return weather_data

      else:
         return "Не удалось получить погоду."

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

   elif callback.data.startswith('weather_'):
      city = callback.data.split('_')[1]
      weather = get_weather(city)
      bot.send_message(callback.message.chat.id, f"🌤️ Погода в {city}:\n{weather}")

   else:  # Обработка и выбора, и ввода города
      process_city(callback.message.chat.id, callback.data)


def process_city_input(message):
   city_name = message.text
   city_info = get_city_info(city_name)
   if city_info:
      description, image_url = city_info
      bot.send_photo(message.chat.id, open(image_url, 'rb'))
      bot.send_message(message.chat.id, f"🏙️ {city_name}\n\n{description}", parse_mode='Markdown')
      
      inline_markup = types.InlineKeyboardMarkup()
      inline_markup.add(types.InlineKeyboardButton('⬅ Назад', callback_data='select_city'))
      inline_markup.add(types.InlineKeyboardButton('🌤 Узнать погоду', callback_data=f'weather_{city_name}'))
      inline_markup.add(types.InlineKeyboardButton('🗺 Посмотреть на карте', url=f'https://www.google.com/maps/search/?q={city_name}&hl=ru'))
      bot.send_message(message.chat.id, "Что дальше?", reply_markup=inline_markup)
   else:
      bot.send_message(message.chat.id, "❗ Город не найден. Попробуйте снова.")


def process_city(chat_id, city):
   """Один метод для обработки как выбранного, так и введенного города."""
   city_info = get_city_info(city)
   if city_info:
      description, image_url = city_info
      bot.send_photo(chat_id, open(image_url, 'rb'))
      bot.send_message(chat_id, f"🏙️ *{city}*\n\n{description}", parse_mode='Markdown')

      inline_markup = types.InlineKeyboardMarkup()
      inline_markup.add(types.InlineKeyboardButton('⬅ Назад', callback_data='select_city'))
      inline_markup.add(types.InlineKeyboardButton('🌤 Узнать погоду', callback_data=f'weather_{city}'))
      inline_markup.add(types.InlineKeyboardButton('🗺 Посмотреть на карте', url=f'https://www.google.com/maps/search/?q={city}&hl=ru'))
      bot.send_message(chat_id, "Что дальше?", reply_markup=inline_markup)
   else:
      bot.send_message(chat_id, "❗ Город не найден. Попробуйте снова.")




# @bot.message_handler(commands=['city'])
# def send_city_info(message):
#     url = "https://www.tripadvisor.ru/Tourism-g298251-Almaty-Vacations.html"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
#     }
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
#         places = []
        
#         for place in soup.find_all("div", class_="JziVN _c"):
#             name_tag = place.find("div", class_="FGwzt ukgoS")
#             rating_tag = place.find("div", class_="biGQs _P pZUbB hmDzD")
#             reviews_tag = place.find("div", class_="nKWJn u qMyjI")
#             desc_tag = place.find("span", class_="biGQs _P pZUbB hmDzD")
#             img_tag = place.find("img")
            
#             if name_tag and rating_tag and reviews_tag and desc_tag and img_tag:
#                 name = name_tag.text.strip()
#                 rating = rating_tag.text.strip()
#                 reviews = reviews_tag.find("div", class_="biGQs _P pZUbB hmDzD").text.strip()
#                 description = desc_tag.text.strip()
#                 img_url = img_tag["src"].split(" ")[0]
                
#                 places.append({
#                     "Название": name,
#                     "Рейтинг": rating,
#                     "Кол-во отзывов": reviews,
#                     "Описание": description,
#                     "Картинка": img_url
#                 })
        
#         for place in places[:5]:  # Ограничение до 5 мест
#             bot.send_message(message.chat.id, f"{place['Название']} ({place['Рейтинг']}) - {place['Кол-во отзывов']} отзывов\nОписание: {place['Описание']}\nКартинка: {place['Картинка']}")
#     else:
#         bot.send_message(message.chat.id, "Ошибка при получении данных с TripAdvisor")


bot.polling(none_stop=True)