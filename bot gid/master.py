import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
import time

TOKEN = 'YOUR_BOT_TOKEN'
api_key = 'YOUR_OPENWEATHERMAP_API_KEY'

bot = telebot.TeleBot(TOKEN)

regions_data = {
    "Северный Казахстан": {"cities": ["Петропавловск", "Кокшетау", "Костанай", "Астана"]},
    "Южный Казахстан": {"cities": ["Шымкент", "Тараз", "Кызылорда", "Туркестан", "Алматы"]},
    "Западный Казахстан": {"cities": ["Атырау", "Уральск", "Актау", "Актобе"]},
    "Восточный Казахстан": {"cities": ["Усть-Каменогорск", "Семей", "Павлодар"]},
    "Центральный Казахстан": {"cities": ["Караганда", "Темиртау", "Балхаш"]}
}

city_info = {
    "Астана": ("Столица Казахстана, известная своей современной архитектурой. Город знаменит своими футуристическими зданиями, такими как Байтерек, Хан Шатыр и Дворец мира и согласия. В Астане проходят важные экономические и культурные форумы мирового уровня. Зимой город превращается в снежную сказку, а летом привлекает гостей своими зелёными парками."),
    "Алматы": ("Крупнейший город Казахстана, окружённый живописными горами Заилийского Алатау. Известен как культурный и финансовый центр страны. Здесь расположены знаменитый высокогорный каток Медео, горнолыжный курорт Шымбулак и смотровая площадка Кок-Тобе. Алматы славится своими зелёными улицами, уютными кафе и богатой историей."),
    "Шымкент": ("Третий по величине город Казахстана, известный своими восточными базарами, гостеприимством и богатой историей. Основанный более 2 200 лет назад, он является одним из древнейших городов региона. Здесь можно посетить этнографический комплекс «Кен-Баба», медресе XIX века и Археологический музей."),
    "Кокшетау": ("Живописный город, окружённый озёрами и лесами. Кокшетау славится своими курортными зонами, такими как Бурабай и Зеренда, привлекающими туристов круглый год. Бурабай часто называют \"Казахстанской Швейцарией\" из-за его горных пейзажей и чистых озёр."),
    "Костанай": ("Город с богатым культурным наследием, расположенный на севере Казахстана. Здесь можно найти исторические памятники, музеи и театры. В регионе развита сельскохозяйственная и промышленная отрасль. В Костанае также проходит ежегодный фестиваль «Тобол-фест», посвящённый народным традициям."),
    "Петропавловск": ("Один из старейших городов Казахстана, основанный в XVIII веке. Здесь сохранилось множество архитектурных памятников, включая Петропавловскую крепость. Город известен своими уютными набережными, а также музеем литературы и искусства, посвящённым творчеству казахских писателей."),
    "Тараз": ("Один из древнейших городов Центральной Азии с историей более 2 000 лет. Тараз славится древними мавзолеями Карахана и Айша-биби, которые являются важными культурными памятниками. Город также называют 'колыбелью казахской цивилизации' за его археологическое и историческое значение."),
    "Кызылорда": ("Город на реке Сырдарья, исторический центр Казахстана. Здесь в XIX веке располагалась первая столица Казахской АССР. Кызылорда также известна как центр казахской национальной письменности и образования, а поблизости находится знаменитый космодром Байконур."),
    "Туркестан": ("Один из самых древних и священных городов Казахстана. Здесь находится мавзолей Ходжи Ахмеда Ясави – объект Всемирного наследия ЮНЕСКО. Туркестан является духовным и культурным центром страны, ежегодно привлекающим тысячи паломников и туристов."),
    "Атырау": ("Нефтяная столица Казахстана, расположенная на реке Урал. Город разделён на две части, европейскую и азиатскую. Атырау известен своими рыбными промыслами, нефтяными месторождениями и современными небоскрёбами."),
    "Уральск": ("Исторический город на западе Казахстана, основанный в XVI веке. Уральск славится своей старинной архитектурой, особенно Казанским собором и домом Пугачёва. Здесь можно посетить музеи, посвящённые истории казачества и древнего Золотого Орды."),
    "Актау": ("Город у Каспийского моря с красивыми пляжами и скалистыми пейзажами. Является важным портовым и туристическим центром. Вблизи города можно посетить урочище Босжира и подземную мечеть Бекет-Ата, считающуюся святыней."),
    "Актобе": ("Динамично развивающийся город на западе Казахстана. Здесь расположены крупные металлургические заводы и современные торговые центры. В окрестностях города можно посетить уникальные геологические образования – меловые горы Актау."),
    "Усть-Каменогорск": ("Город металлургов, расположенный среди гор Восточного Казахстана. Он известен своими красивыми природными пейзажами, такими как Бухтарминское водохранилище и национальный парк Катон-Карагай."),
    "Семей": ("Исторический город, связанный с именем Абая Кунанбаева. В Семее расположен музей Абая, старейшая мечеть Казахстана и мост через Иртыш – один из самых длинных в Центральной Азии."),
    "Павлодар": ("Город с развитой промышленностью и живописными набережными. Павлодар известен своими современными театрами, музеями и близостью к национальному парку Баянаул."),
    "Караганда": ("Крупный промышленный центр Казахстана, связанный с угольной промышленностью. Город славится своим театром имени Станиславского и парком Ботанический сад. Недалеко находится музей ГУЛАГа в поселке Долинка."),
    "Темиртау": ("Город металлургов, важный центр чёрной металлургии Казахстана. Здесь находится крупнейший металлургический завод страны. Также город известен своим ледовым дворцом и живописной набережной реки Нура."),
    "Балхаш": ("Город на берегу одноимённого озера, которое наполовину пресное, наполовину солёное. Балхаш привлекает туристов своими пляжами, рыбалкой и уникальной природой.")
}

city_images = {
    "Астана": "A:/yer4ss/Work/im python/bot gid/images/Астана.jpg",
    "Алматы": "A:/yer4ss/Work/im python/bot gid/images/Алматы.jpg",
    "Шымкент": "A:/yer4ss/Work/im python/bot gid/images/Шымкент.jpg",
    "Кокшетау": "A:/yer4ss/Work/im python/bot gid/images/Кокшетау.jpg",
    "Костанай": "A:/yer4ss/Work/im python/bot gid/images/Костанай.jpg",
    "Петропавловск": "A:/yer4ss/Work/im python/bot gid/images/Петропавловск.jpg",
    "Тараз": "A:/yer4ss/Work/im python/bot gid/images/Тараз.jpg",
    "Кызылорда": "A:/yer4ss/Work/im python/bot gid/images/Кызылорда.jpg",
    "Туркестан": "A:/yer4ss/Work/im python/bot gid/images/Туркестан.jpg",
    "Атырау": "A:/yer4ss/Work/im python/bot gid/images/Атырау.jpg",
    "Уральск": "A:/yer4ss/Work/im python/bot gid/images/Уральск.jpg",
    "Актау": "A:/yer4ss/Work/im python/bot gid/images/Актау.jpg",
    "Актобе": "A:/yer4ss/Work/im python/bot gid/images/Актобе.jpg",
    "Усть-Каменогорск": "A:/yer4ss/Work/im python/bot gid/images/Усть-Каменогорск.jpg",
    "Семей": "A:/yer4ss/Work/im python/bot gid/images/Семей.jpg",
    "Павлодар": "A:/yer4ss/Work/im python/bot gid/images/Павлодар.jpg",
    "Караганда": "A:/yer4ss/Work/im python/bot gid/images/Караганда.jpg",
    "Темиртау": "A:/yer4ss/Work/im python/bot gid/images/Темиртау.jpg",
    "Балхаш": "A:/yer4ss/Work/im python/bot gid/images/Балхаш.jpg"
}

city_maps = {
    "Астана": "https://www.google.com/maps/search/?q=Астана&hl=ru",
    "Алматы": "https://www.google.com/maps/search/?q=Алматы&hl=ru",
    "Шымкент": "https://www.google.com/maps/search/?q=Шымкент&hl=ru",
    "Кокшетау": "https://www.google.com/maps/search/?q=Кокшетау&hl=ru",
    "Костанай": "https://www.google.com/maps/search/?q=Костанай&hl=ru",
    "Петропавловск": "https://www.google.com/maps/search/?q=Петропавловск&hl=ru",
    "Тараз": "https://www.google.com/maps/search/?q=Тараз&hl=ru",
    "Кызылорда": "https://www.google.com/maps/search/?q=Кызылорда&hl=ru",
    "Туркестан": "https://www.google.com/maps/search/?q=Туркестан&hl=ru",
    "Атырау": "https://www.google.com/maps/search/?q=Атырау&hl=ru",
    "Уральск": "https://www.google.com/maps/search/?q=Уральск&hl=ru",
    "Актау": "https://www.google.com/maps/search/?q=Актау&hl=ru",
    "Актобе": "https://www.google.com/maps/search/?q=Актобе&hl=ru",
    "Усть-Каменогорск": "https://www.google.com/maps/search/?q=Усть-Каменогорск&hl=ru",
    "Семей": "https://www.google.com/maps/search/?q=Семей&hl=ru",
    "Павлодар": "https://www.google.com/maps/search/?q=Павлодар&hl=ru",
    "Караганда": "https://www.google.com/maps/search/?q=Караганда&hl=ru",
    "Темиртау": "https://www.google.com/maps/search/?q=Темиртау&hl=ru",
    "Балхаш": "https://www.google.com/maps/search/?q=Балхаш&hl=ru"
}

categories = {
    "Куда можно сходить": ["Парки", "Кафе", "Рестораны", "Торговые центры"],
    "Где можно переночевать": ["Мотели", "Отели", "Съёмные квартиры"]
}

places_data = {
    "Астана": {
        "Парки": {"Парк Атамекен": "ул. Тауелсиздик 1", "Президентский парк": "пр. Туран 57"},
        "Кафе": {"Кафе Астана": "ул. Сарыарка 10", "Кофейня Relax": "пр. Кабанбай батыра 22"},
        "Рестораны": {"Satti": "ул. Кунаева 14", "Line Brew": "ул. Бейбитшилик 3"},
        "Торговые центры": {"Хан Шатыр": "пр. Туран 37", "MEGA Silk Way": "пр. Кабанбай батыра 62"}
    },
    "Алматы": {
        "Парки": {"Парк Панфилова": "ул. Калдаякова 22", "Кок Тобе": "ул. Достык 104"},
        "Кафе": {"Кафе Del Papa": "пр. Абая 30", "Traveler's Coffee": "ул. Сатпаева 30"},
        "Рестораны": {"Daredzhani": "ул. Жамбыла 77", "BarFly": "ул. Байтурсынова 101"},
        "Торговые центры": {"Dostyk Plaza": "ул. Сатпаева 111", "MEGA Park": "пр. Сейфуллина 58"}
    },
    "Шымкент": {
        "Парки": {"Парк Абая": "ул. Дулати 5", "Парк Жибек Жолы": "пр. Республики 8"},
        "Кафе": {"Кафе Central": "ул. Байтерекова 20", "Korzinka Coffee": "пр. Кунаева 12"},
        "Рестораны": {"Казахская Юрта": "ул. Толе би 18", "Aladdin": "ул. Абая 47"},
        "Торговые центры": {"Шымкент Plaza": "ул. Рыскулова 12", "Фиркан City": "ул. Тауке хана 45"}
    }
}

# Кеш погоды
weather_cache = {}
CACHE_TIMEOUT = 600  # 10 минут

# Сохранённые избранные места
user_favorites = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    for region in regions_data:
        markup.add(InlineKeyboardButton(region, callback_data=region))
    bot.send_message(message.chat.id, "Выберите регион:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Не  суетись да, братишка жи ес, я тебе здесь не поддержка канкретно.")

@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, "Этот бот канкретно жи ес делает прогулка канкретно по городам Казахстана.\n"
                                        "Суету делает канкретно жи ес, понял да жи ес!?.\n"
                                        "Выбираешь канкретно местность и город, и бот канкретно жи ес показывает фото и описание канкретно жи ес.")

# Функция для получения погоды с кешем
def get_weather(city):
    current_time = time.time()
    if city in weather_cache and current_time - weather_cache[city]['time'] < CACHE_TIMEOUT:
        return weather_cache[city]['data']
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url).json()
    if response.get("main"):
        weather_desc = response['weather'][0]['description']
        temp = response['main']['temp']
        wind = response['wind']['speed']
        humidity = response['main']['humidity']
        weather_data = f"{weather_desc.capitalize()}\n| Температура: {temp}°C\n| Ветер: {wind} м/с\n| Влажность: {humidity}%"
        weather_cache[city] = {'data': weather_data, 'time': current_time}
        return weather_data
    else:
        return "Не удалось получить погоду."


@bot.callback_query_handler(func=lambda call: call.data in regions_data)
def select_region(call):
    region = call.data
    markup = InlineKeyboardMarkup()
    for city in regions_data[region]:
        markup.add(InlineKeyboardButton(city, callback_data=city))
    markup.add(InlineKeyboardButton("* Выбрать другой регион *", callback_data="back"))
    bot.edit_message_text(f"Вы выбрали регион {region}. Выберите город:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    select_region(call.message)

@bot.callback_query_handler(func=lambda call: call.data in city_info)
def select_city(call):
    city = call.data
    info, img_path = city_info[city]
    weather = get_weather(city)
    with open(img_path, "rb") as photo:
        bot.send_photo(call.message.chat.id, photo, caption=f"{city}: {info}\n\n Погода: {weather}")

# Обработчик выбора категории
@bot.callback_query_handler(func=lambda call: call.data.startswith("category"))
def show_places(call):
    _, city, category = call.data.split("_")
    places = places_data.get(city, {}).get(category, {})
    for place, address in places.items():
        bot.send_message(call.message.chat.id, f"{place}\nАдрес: {address}\n[Смотреть на карте](https://www.google.com/maps/search/{place.replace(' ', '+')})", parse_mode="Markdown")
    bot.send_message(call.message.chat.id, "Выберите ещё место или вернитесь назад:", reply_markup=create_buttons(categories.keys(), "category", city))

# Универсальная функция для создания кнопок

def create_buttons(buttons_data, prefix, city=None):
    markup = types.InlineKeyboardMarkup()
    for item in buttons_data:
        callback_data = f"{prefix}_{item}" if city is None else f"{prefix}_{city}_{item}"
        markup.add(types.InlineKeyboardButton(item, callback_data=callback_data))
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))
    return markup

bot.polling(none_stop=True)