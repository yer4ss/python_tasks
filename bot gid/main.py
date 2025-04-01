import requests
from bs4 import BeautifulSoup
from io import BytesIO
import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("8137093677:AAFk7pvkeH819sk5nLPLkanJD774U6WHYCg")
user_data = {}

def get_trip_info(city_name):
    """Получаем trip_code и trip_name из базы данных."""
    conn = sqlite3.connect("cities.db")
    cursor = conn.cursor()
    cursor.execute("SELECT trip_code, trip_name FROM cities WHERE name = ?", (city_name,))
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

@bot.message_handler(commands=['city'])
def ask_city(message):
    bot.send_message(message.chat.id, "Введите название города:")
    bot.register_next_step_handler(message, process_city)

def process_city(message):
    city_name = message.text.strip()
    trip_code, trip_name = get_trip_info(city_name)
    
    if trip_code and trip_name:
        user_data[message.chat.id] = (trip_code, trip_name)
        send_places(message, trip_code, trip_name)
    else:
        bot.send_message(message.chat.id, "❌ Город не найден в базе.")

def send_places(message, trip_code, trip_name):
    url = f"https://www.tripadvisor.ru/Tourism-{trip_code}-{trip_name}-Vacations.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        bot.send_message(message.chat.id, "❌ Ошибка при получении данных.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.find_all("div", class_="AOgUr")
    section_titles = {"Чем заняться": "attractions", "Где остановиться": "hotels", "Еда и напитки": "restaurants"}
    
    markup = types.InlineKeyboardMarkup()
    for title, command in section_titles.items():
        markup.add(types.InlineKeyboardButton(title, callback_data=command))
    
    bot.send_message(message.chat.id, "Что вас интересует?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["attractions", "hotels", "restaurants"])
def callback_query(call):
    chat_id = call.message.chat.id
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "❌ Сначала выберите город через /city.")
        return
    
    trip_code, trip_name = user_data[chat_id]
    url = f"https://www.tripadvisor.ru/Tourism-{trip_code}-{trip_name}-Vacations.html"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code != 200:
        bot.send_message(chat_id, "❌ Ошибка при получении данных.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.find_all("div", class_="AOgUr")
    section_titles = {"Чем заняться": "attractions", "Где остановиться": "hotels", "Еда и напитки": "restaurants"}
    
    target_section = None
    for section in sections:
        title_tag = section.find("h3", class_="biGQs _P fiohW uuBRH")
        if title_tag and section_titles.get(title_tag.text.strip()) == call.data:
            target_section = section
            break
    
    if not target_section:
        bot.send_message(chat_id, f"⚠ Раздел '{call.data}' не найден.")
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
        
        places.append({"Название": name, "Рейтинг": rating, "Кол-во отзывов": reviews, "Описание": description, "Картинка": img_url})

    if places:
        for place in places:  
            if place["Картинка"]:
                img_response = requests.get(place["Картинка"])
                if img_response.status_code == 200:
                    bot.send_photo(chat_id, BytesIO(img_response.content))
            
            bot.send_message(chat_id, f"🏙️ {place['Название']} ({place['Рейтинг']})\n📌 {place['Кол-во отзывов']} отзывов\n📖 {place['Описание']}")
    else:
        bot.send_message(chat_id, f"⚠ В разделе '{call.data}' нет мест.")

bot.polling(none_stop=True)