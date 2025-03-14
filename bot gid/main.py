import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
import config
import requests

bot = telebot.TeleBot(config.token)
api_key = "17697edb22cd6287f4a12ccb3e497513"

regions = {
   "Северный Казахстан": ["Петропавловск", "Кокшетау", "Костанай", "Астана"],
   "Южный Казахстан": ["Шымкент", "Тараз", "Кызылорда", "Туркестан", "Алматы"],
   "Западный Казахстан": ["Атырау", "Уральск", "Актау", "Актобе"],
   "Восточный Казахстан": ["Усть-Каменогорск", "Семей", "Павлодар"],
   "Центральный Казахстан": ["Караганда", "Темиртау", "Балхаш"]
}

city_info = {
   "Астана": ("Столица Казахстана, известная своей современной архитектурой. Город знаменит своими футуристическими зданиями, такими как Байтерек, Хан Шатыр и Дворец мира и согласия. В Астане проходят важные экономические и культурные форумы мирового уровня. Зимой город превращается в снежную сказку, а летом привлекает гостей своими зелёными парками.", 
               "A:/yer4ss/Work/im python/bot gid/images/Астана.jpg"),
   "Алматы": ("Крупнейший город Казахстана, окружённый живописными горами Заилийского Алатау. Известен как культурный и финансовый центр страны. Здесь расположены знаменитый высокогорный каток Медео, горнолыжный курорт Шымбулак и смотровая площадка Кок-Тобе. Алматы славится своими зелёными улицами, уютными кафе и богатой историей.", 
               "A:/yer4ss/Work/im python/bot gid/images/Алматы.jpg"),
   "Шымкент": ("Третий по величине город Казахстана, известный своими восточными базарами, гостеприимством и богатой историей. Основанный более 2 200 лет назад, он является одним из древнейших городов региона. Здесь можно посетить этнографический комплекс «Кен-Баба», медресе XIX века и Археологический музей.", 
               "A:/yer4ss/Work/im python/bot gid/images/Шымкент.jpg"),
   "Кокшетау": ("Живописный город, окружённый озёрами и лесами. Кокшетау славится своими курортными зонами, такими как Бурабай и Зеренда, привлекающими туристов круглый год. Бурабай часто называют \"Казахстанской Швейцарией\" из-за его горных пейзажей и чистых озёр.", 
               "A:/yer4ss/Work/im python/bot gid/images/Кокшетау.jpg"),
   "Костанай": ("Город с богатым культурным наследием, расположенный на севере Казахстана. Здесь можно найти исторические памятники, музеи и театры. В регионе развита сельскохозяйственная и промышленная отрасль. В Костанае также проходит ежегодный фестиваль «Тобол-фест», посвящённый народным традициям.", 
               "A:/yer4ss/Work/im python/bot gid/images/Костанай.jpg"),
   "Петропавловск": ("Один из старейших городов Казахстана, основанный в XVIII веке. Здесь сохранилось множество архитектурных памятников, включая Петропавловскую крепость. Город известен своими уютными набережными, а также музеем литературы и искусства, посвящённым творчеству казахских писателей.", 
               "A:/yer4ss/Work/im python/bot gid/images/Петропавловск.jpg"),
   "Тараз": ("Один из древнейших городов Центральной Азии с историей более 2 000 лет. Тараз славится древними мавзолеями Карахана и Айша-биби, которые являются важными культурными памятниками. Город также называют 'колыбелью казахской цивилизации' за его археологическое и историческое значение.", 
               "A:/yer4ss/Work/im python/bot gid/images/Тараз.jpg"),
   "Кызылорда": ("Город на реке Сырдарья, исторический центр Казахстана. Здесь в XIX веке располагалась первая столица Казахской АССР. Кызылорда также известна как центр казахской национальной письменности и образования, а поблизости находится знаменитый космодром Байконур.", 
               "A:/yer4ss/Work/im python/bot gid/images/Кызылорда.jpg"),
   "Туркестан": ("Один из самых древних и священных городов Казахстана. Здесь находится мавзолей Ходжи Ахмеда Ясави – объект Всемирного наследия ЮНЕСКО. Туркестан является духовным и культурным центром страны, ежегодно привлекающим тысячи паломников и туристов.", 
               "A:/yer4ss/Work/im python/bot gid/images/Туркестан.jpg"),
   "Атырау": ("Нефтяная столица Казахстана, расположенная на реке Урал. Город разделён на две части, европейскую и азиатскую. Атырау известен своими рыбными промыслами, нефтяными месторождениями и современными небоскрёбами.", 
               "A:/yer4ss/Work/im python/bot gid/images/Атырау.jpg"),
   "Уральск": ("Исторический город на западе Казахстана, основанный в XVI веке. Уральск славится своей старинной архитектурой, особенно Казанским собором и домом Пугачёва. Здесь можно посетить музеи, посвящённые истории казачества и древнего Золотого Орды.", 
               "A:/yer4ss/Work/im python/bot gid/images/Уральск.jpg"),
   "Актау": ("Город у Каспийского моря с красивыми пляжами и скалистыми пейзажами. Является важным портовым и туристическим центром. Вблизи города можно посетить урочище Босжира и подземную мечеть Бекет-Ата, считающуюся святыней.", 
               "A:/yer4ss/Work/im python/bot gid/images/Актау.jpg"),
   "Актобе": ("Динамично развивающийся город на западе Казахстана. Здесь расположены крупные металлургические заводы и современные торговые центры. В окрестностях города можно посетить уникальные геологические образования – меловые горы Актау.", 
               "A:/yer4ss/Work/im python/bot gid/images/Актобе.jpg"),
   "Усть-Каменогорск": ("Город металлургов, расположенный среди гор Восточного Казахстана. Он известен своими красивыми природными пейзажами, такими как Бухтарминское водохранилище и национальный парк Катон-Карагай.", 
               "A:/yer4ss/Work/im python/bot gid/images/Усть-Каменогорск.jpg"),
   "Семей": ("Исторический город, связанный с именем Абая Кунанбаева. В Семее расположен музей Абая, старейшая мечеть Казахстана и мост через Иртыш – один из самых длинных в Центральной Азии.", 
               "A:/yer4ss/Work/im python/bot gid/images/Семей.jpg"),
   "Павлодар": ("Город с развитой промышленностью и живописными набережными. Павлодар известен своими современными театрами, музеями и близостью к национальному парку Баянаул.", 
               "A:/yer4ss/Work/im python/bot gid/images/Павлодар.jpg"),
   "Караганда": ("Крупный промышленный центр Казахстана, связанный с угольной промышленностью. Город славится своим театром имени Станиславского и парком Ботанический сад. Недалеко находится музей ГУЛАГа в поселке Долинка.", 
               "A:/yer4ss/Work/im python/bot gid/images/Караганда.jpg"),
   "Темиртау": ("Город металлургов, важный центр чёрной металлургии Казахстана. Здесь находится крупнейший металлургический завод страны. Также город известен своим ледовым дворцом и живописной набережной реки Нура.", 
               "A:/yer4ss/Work/im python/bot gid/images/Темиртау.jpg"),
   "Балхаш": ("Город на берегу одноимённого озера, которое наполовину пресное, наполовину солёное. Балхаш привлекает туристов своими пляжами, рыбалкой и уникальной природой.", 
               "A:/yer4ss/Work/im python/bot gid/images/Балхаш.jpg")
}

def get_weather(city):
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
   response = requests.get(url).json()
   if response.get("main"):
      weather_desc = response['weather'][0]['description']
      temp = response['main']['temp']
      wind = response['wind']['speed']
      humidity = response['main']['humidity']
      return f"{weather_desc.capitalize()}\n| Температура: {temp}°C\n| Ветер: {wind} м/с\n| Влажность: {humidity}%"
   else:
      return "Не удалось получить погоду."

@bot.message_handler(commands=['start'])
def start(message):
   markup = InlineKeyboardMarkup()
   for region in regions:
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

@bot.message_handler(commands=['menu'])
def show_menu(message):
   markup = ReplyKeyboardMarkup(resize_keyboard=True)
   markup.add(KeyboardButton("/start"), KeyboardButton("/help"), KeyboardButton("/about"))
   bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in regions)
def select_region(call):
   region = call.data
   markup = InlineKeyboardMarkup()
   for city in regions[region]:
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



bot.polling(none_stop=True)

# if __name__ == "__main__":
#    bot.infinity_polling()