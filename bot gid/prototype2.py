import telebot
from telebot import types
import os
import requests
import time
import sqlite3
from bs4 import BeautifulSoup
from io import BytesIO


bot = telebot.TeleBot('7780668347:AAFTwSbXzNg02naVu_g2x-k2GiPiYPVlOng')


@bot.message_handler(commands=['start', 'stop', 'help', 'about'])
def handle_commands(message):
   if message.text == '/start':
      command_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      command_markup.row('/start', '/stop')
      command_markup.row('/help', '/about')

      bot.send_message(message.chat.id, 
                        f"Привет, {message.from_user.first_name}! 👋\n"
                        "Я - твой персональный гид по Казахстану! 🇰🇿\n"
                        "Могу показать тебе интересные места, рассказать факты и подсказать погоду. 🌍✨", reply_markup=command_markup)

      inline_markup = types.InlineKeyboardMarkup()
      btn1 = types.InlineKeyboardButton('Выбрать город', callback_data='city_list')
      btn2 = types.InlineKeyboardButton('Ввести название', callback_data='input_city')
      inline_markup.row(btn1, btn2)

      bot.send_message(message.chat.id, "Для начала выбери действие:", reply_markup=inline_markup)

   elif message.text == '/help':
      bot.send_message(message.chat.id, 
                        "<b>Мои команды:</b>\n"
                        "/start — начать общение с ботом\n"
                        "/help — получить справку о боте\n"
                        "/about — узнать информацию о разработчике\n"
                        "/stop — завершить общение с ботом", parse_mode='html')

   elif message.text == '/about':
      bot.send_message(message.chat.id, 
                        "Этот бот был создан в рамках проекта по изучению Python и Telegram API.\n"
                        "Разработчик: <em><b>yerazz</b></em>", parse_mode='html')

   elif message.text == '/stop':
      bot.send_message(message.chat.id, "До свидания! Бот остановлен и больше не реагирует на сообщения.")
      os._exit(0)



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
            f" {weather_desc.capitalize()}\n"
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



def get_city_info(name):
   conn = sqlite3.connect('cities.db')
   cursor = conn.cursor()
   cursor.execute('SELECT description, image_url, trip_code, trip_name FROM cities WHERE name = ?', (name,))
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
user_data = {}



@bot.message_handler(commands=['attractions', 'hotels', 'restaurants'])
def send_places(message, trip_code, trip_name, category):
    chat_id = message.chat.id if message else callback.message.chat.id

    if trip_code is None or trip_name is None:
        user_info = user_data.get(chat_id)
        if not user_info:
            bot.send_message(chat_id, "⚠ Сначала выберите город.")
            return
        trip_code, trip_name = user_info["trip_code"], user_info["trip_name"]


    url = f"https://www.tripadvisor.ru/Tourism-{trip_code}-{trip_name}-Vacations.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        sections = soup.find_all("div", class_="AOgUr")

        # Соответствие заголовков и команд
        section_titles = {
            "Чем заняться": "attractions",
            "Где остановиться": "hotels",
            "Еда и напитки": "restaurants"
        }

        # Определяем, какая команда была вызвана
        command = category
        target_section = None

        # Ищем нужный раздел по заголовку <h3>
        for section in sections:
            title_tag = section.find("h3", class_="biGQs _P fiohW uuBRH")  # Заголовок секции
            if title_tag and title_tag.text.strip() in section_titles:
                if section_titles[title_tag.text.strip()] == command:
                    target_section = section
                    break

        if not target_section:
            bot.send_message(message.chat.id, f"⚠ Раздел '{command}' не найден.")
            return

        places = []
        for place in target_section.find_all("div", class_="JziVN _c")[:3]:
            name_tag = place.find("div", class_="FGwzt ukgoS")
            rating_tag = place.find("div", class_="biGQs _P pZUbB hmDzD")
            reviews_tag = place.find("div", class_="nKWJn u qMyjI")
            desc_tag = place.find("span", class_="biGQs _P pZUbB hmDzD")
            img_tag = place.find("img")

            name = name_tag.text.strip() if name_tag else "Без названия"
            rating = rating_tag.text.strip() if rating_tag else "Рейтинг отсутствует"
            reviews = reviews_tag.find("div", class_="biGQs _P pZUbB hmDzD").text.strip() if reviews_tag else "Нет отзывов"
            description = desc_tag.text.strip() if desc_tag else "Описание отсутствует"
            img_url = img_tag["src"].split(" ")[0] if img_tag else None

            places.append({
                "Название": name,
                "Рейтинг": rating,
                "Кол-во отзывов": reviews,
                "Описание": description,
                "Картинка": img_url
            })

        if places:
            for place in places:  
                if place["Картинка"]:
                    img_response = requests.get(place["Картинка"])
                    if img_response.status_code == 200:
                        image = BytesIO(img_response.content)
                        bot.send_photo(message.chat.id, image)
                
                bot.send_message(
                    message.chat.id, 
                    f"🏙️ {place['Название']} ({place['Рейтинг']})\n"
                    f"📌 {place['Кол-во отзывов']} отзывов\n"
                    f"📖 {place['Описание']}"
                )
        else:
            bot.send_message(message.chat.id, f"⚠ В разделе '{command}' нет мест.")
    else:
        bot.send_message(message.chat.id, "❌ Ошибка при получении данных.")
    
    back_markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("⬅ Назад к городу", callback_data="back_to_city")
    back_markup.add(back_btn)

    bot.send_message(message.chat.id, "Если хотите вернуться", reply_markup=back_markup)



@bot.callback_query_handler(func=lambda call: True)
def callback(callback):
    chat_id = callback.message.chat.id

    # Обработка выбора города
    if callback.data == 'city_list':
        markup = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(city, callback_data=city) for city in cities]
        for i in range(0, len(buttons), 3):
            markup.row(*buttons[i:i+3])

        bot.send_message(chat_id, "Выбери город из списка:", reply_markup=markup)

    # Обработка запроса на ввод города
    elif callback.data == 'input_city':
        msg = bot.send_message(chat_id, "Введите название города:")
        bot.register_next_step_handler(msg, lambda m: process_city(m.chat.id, m.text))

    # Обработка запроса на погоду
    elif callback.data.startswith('weather_'):
        city = callback.data.split('_')[1]
        weather = get_weather(city)
        bot.send_message(chat_id, f"🌤️ Погода в {city}: {weather}")

    # Обработка выбора города из списка
    elif callback.data in cities:
        process_city(chat_id, callback.data)

    # Обработка выбора разделов: достопримечательности, отели, рестораны
    elif callback.data in ['attractions', 'hotels', 'restaurants']:
        user_info = user_data.get(chat_id)
        if user_info:
            send_places(callback.message, user_info["trip_code"], user_info["trip_name"], callback.data)
        else:
            bot.send_message(chat_id, "⚠ Сначала выберите город.")

    elif callback.data == "back_to_city":
        user_info = user_data.get(chat_id)
        if user_info:
            process_city(chat_id, user_info["city_name"])
        else:
            bot.send_message(chat_id, "⚠ Сначала выберите город.")


    else:
        bot.send_message(chat_id, "❗ Неизвестная команда. Попробуйте снова.")



def process_city(chat_id, city_name):
    city_info = get_city_info(city_name)

    if city_info:
        description, image_url, trip_code, trip_name = city_info
        
        # Сохраняем данные города в user_data
        user_data[chat_id] = {"city_name": city_name, "trip_code": trip_code, "trip_name": trip_name}

        # Отправляем фото и описание города
        bot.send_photo(chat_id, open(image_url, 'rb'))
        bot.send_message(chat_id, f"🏙️ {city_name}\n\n{description}", parse_mode='Markdown')

        # Создаем кнопки для дальнейшего выбора
        inline_markup = types.InlineKeyboardMarkup()
        weather_btn = types.InlineKeyboardButton('🌤 Узнать погоду', callback_data=f'weather_{city_name}')
        map_btn = types.InlineKeyboardButton('🗺 Посмотреть на карте', url=f'https://www.google.com/maps/search/?q={city_name}&hl=ru')
        inline_markup.row(weather_btn, map_btn)

        inline_markup.row(
            types.InlineKeyboardButton('🏛️ Достопримечательности', callback_data='attractions'),
            types.InlineKeyboardButton('🏨 Отели', callback_data='hotels'),
            types.InlineKeyboardButton('🍽️ Рестораны', callback_data='restaurants')
        )

        inline_markup.add(types.InlineKeyboardButton('⬅ Назад', callback_data='city_list'))

        bot.send_message(chat_id, "Что вас интересует?", reply_markup=inline_markup)
    
    else:
        bot.send_message(chat_id, "❗ Город не найден. Попробуйте снова.")


bot.polling(none_stop=True)