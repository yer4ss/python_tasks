import telebot
import webbrowser
from telebot import types
import os

bot = telebot.TeleBot('7780668347:AAFTwSbXzNg02naVu_g2x-k2GiPiYPVlOng')
# api_key = '17697edb22cd6287f4a12ccb3e497513'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()                                             # кнопки под клавой
    btn1 = types.KeyboardButton('/start')
    btn2 = types.KeyboardButton('/help')
    btn3 = types.KeyboardButton('/about')
    btn4 = types.KeyboardButton('/map')
    markup.row(btn1, btn2, btn3)
    markup.add(btn4)

    bot.send_message(message.chat.id, 'Hello', reply_markup=markup)


    markup = types.InlineKeyboardMarkup()                                             # кнопки под сообщением
    markup.add(types.InlineKeyboardButton('Google', url='https://www.google.com'))
    markup.add(types.InlineKeyboardButton('wasd', callback_data='wasd'))             # callback вызывает функцию  

    btn2 = types.InlineKeyboardButton('edit', callback_data='edit_text')
    btn3 = types.InlineKeyboardButton('delete', callback_data='delete_text')
    markup.row(btn2, btn3)                                                      # создает кнопки в одну строку   

    bot.send_message(message.chat.id, 'text', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)       # обрабатывает кнопку, lambda - анонимная функция
def callback_nahuy(callback):
    if callback.data == 'wasd':
        bot.send_message(callback.message.chat.id, 'wasd')
    elif callback.data == 'edit_text':
        bot.edit_message_text('edited', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'delete_text':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)   # удаляет предпоследнее сообщение в чате


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>I</b> <em>can help</em> <u>you</u>!', parse_mode='html')


@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['map', 'location'])                 # открывает карту
def map(message):
    webbrowser.open('https://www.google.com/maps')


@bot.message_handler(commands=['stop'])
def stop(message):
    chat_id = message.chat.id

    # Удаляем последние 20 сообщений (можно увеличить)
    for i in range(message.message_id - 20, message.message_id + 1):
        try:
            bot.delete_message(chat_id, i)
        except Exception as e:
            print(f"Не удалось удалить сообщение {i}: {e}")

    bot.send_message(chat_id, "До свидания! Если захочешь поговорить, пиши /start.")
    os._exit(0)


@bot.message_handler(content_types=['text'])             # обрабатывает сообщения простым текстом
def text(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!')
    elif message.text.lower() == 'bye':
        bot.send_message(message.chat.id, f'Bye, {message.from_user.first_name}!')


bot.polling(none_stop=True)