import telebot
from telebot import types
import sqlite3

TOKEN = '7780668347:AAFTwSbXzNg02naVu_g2x-k2GiPiYPVlOng'
bot = telebot.TeleBot(TOKEN)

# Функция для получения информации о городе
def get_city_info(name):
    conn = sqlite3.connect('cities.db')
    cursor = conn.cursor()
    cursor.execute('SELECT description, image_url FROM cities WHERE name = ?', (name,))
    result = cursor.fetchone()
    conn.close()
    return result

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот-гид по городам Казахстана. Выбери город, чтобы узнать больше!")

# Команда для выбора города
@bot.message_handler(commands=['cities'])
def show_cities(message):
    conn = sqlite3.connect('cities.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM cities')
    cities = cursor.fetchall()
    conn.close()

    # Создаем кнопки с названиями городов
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for city in cities:
        markup.add(types.KeyboardButton(city[0]))

    bot.send_message(message.chat.id, "Выберите город:", reply_markup=markup)

# Обработка выбора города
@bot.message_handler(func=lambda message: True)
def send_city_info(message):
    city_name = message.text
    city_info = get_city_info(city_name)

    if city_info:
        description, image_url = city_info
        bot.send_photo(message.chat.id, open(image_url, 'rb'))
        bot.send_message(message.chat.id, f"🏙️ *{city_name}*\n\n{description}", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❗ Город не найден в базе. Попробуйте другой.")

# Запуск бота
bot.polling(none_stop=True)
