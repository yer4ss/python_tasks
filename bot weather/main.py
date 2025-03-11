import telebot
import requests
import config

bot = telebot.TeleBot(config.token)

api_key = "апишка"

@bot.message_handler(content_types=["text"])
def handle_text(message):
   city = message.text
   return city

def get_weather():

   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
   data = requests.get(url).json()
   temp = data["main"]["temp"]
   wind = data["wind"]["speed"]
   humidity = data["main"]["humidity"]
   pressure = data["main"]["pressure"]
   description = data["weather"][0]["description"]
   cloudiness = data["clouds"]["all"]

   return f"| Температура: {temp}°C\n| Ветер: {wind} m/s\n| Влажность: {humidity}%\n| Давление: {pressure} hPa\n| Описание: {description.capitalize()}\n| Облачность: {cloudiness}%"

@bot.message_handler(commands=["start"])
def send_weather(message):
   bot.send_message(message.chat.id, get_weather())

bot.polling()