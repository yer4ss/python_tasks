import telebot
import config
import random
import time

bot = telebot.TeleBot(config.token)

badWords = ['лэбэнь, дурак, идиот, тупой, дурачок, дурачка, дурачок, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дурачатина, дурачатник, дурачатница, дурачаты, дурачыч, дурачыш, дурачонок, дураченок, дура']

@bot.message_handler(commands=['start'])
def start_spam(message):
   for _ in range(10):
         random_word = random.choice(badWords)
         bot.send_message(message.chat.id, f"{random_word}")
         time.sleep(1) 
   bot.send_message(message.chat.id, "*БЕЗ НЕГАТИВА)*")
   
if __name__ == "__main__":
   bot.infinity_polling()