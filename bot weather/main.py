import telebot
import requests
import config

bot = telebot.TeleBot(config.token)

api_key = "3f9a6b1234567890abcdef1234567890"

@bot.message_handler(commands=["start"])
def send_weather(message):
   bot.send_message(message.chat.id, "Введите название города на английском языке:")

@bot.message_handler(content_types=["text"])
def get_weather(message):
   city = message.text
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
   data = requests.get(url).json()
   temp = data["main"]["temp"]
   wind = data["wind"]["speed"]
   humidity = data["main"]["humidity"]
   pressure = data["main"]["pressure"]
   description = data["weather"][0]["description"]
   cloudiness = data["clouds"]["all"]

   weather_info = (f"| Температура: {temp}°C\n| Ветер: {wind} m/s\n| Влажность: {humidity}%\n| Давление: {pressure} hPa\n| Описание: {description.capitalize()}\n| Облачность: {cloudiness}%")

   bot.send_message(message.chat.id, weather_info)

bot.polling()