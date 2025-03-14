import telebot
import requests
from telebot import types
import config

bot = telebot.TeleBot(config.token)
api_key = "17697edb22cd6287f4a12ccb3e497513"

cities = ["Алматы", "Нур-Султан", "Шымкент", "Караганда", "Актобе"]

@bot.message_handler(commands=["start"])
def send_city_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for city in cities:
        markup.add(types.KeyboardButton(city))
    bot.send_message(message.chat.id, "Выберите город для прогноза погоды:", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text
    if city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
        data = requests.get(url).json()
        
        if data.get("main"):
            temp = data["main"]["temp"]
            wind = data["wind"]["speed"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            description = data["weather"][0]["description"]
            cloudiness = data["clouds"]["all"]

            weather_info = (f"| Температура: {temp}°C\n| Ветер: {wind} м/с\n| Влажность: {humidity}%\n"
                            f"| Давление: {pressure} hPa\n| Описание: {description.capitalize()}\n| Облачность: {cloudiness}%")
            bot.send_message(message.chat.id, weather_info)
        else:
            bot.send_message(message.chat.id, "Не удалось получить погоду. Попробуйте снова.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите город с кнопок!")

bot.polling(none_stop=True)
