import telebot
import time
import requests
import json

bot = telebot.TeleBot("TOKEN")

def findat(msg):
    for i in msg:
        if 'https://www.radiojavan.com/mp3s/mp3/' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Hello, For help just type /help')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'Enter your RadioJavan link to get the lyric and mp3 link\nExample: https://www.radiojavan.com/mp3s/mp3/Ali-Sorena-Gonjeshkaka')

@bot.message_handler(func=lambda msg: msg.text is not None and 'https://www.radiojavan.com/mp3s/mp3/' in msg.text)

def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == 'https://www.radiojavan.com': # in case it's just the '@', skip
        pass
    else:

        insta_link = "https://api-rj-app.com/api2/mp3?id={}".format(at_text[36:])

        data = requests.get(insta_link).text
        data = json.loads(data)

        lyric = data["lyric"]
        link = data["link"]

        bot.reply_to(message, lyric)
        bot.reply_to(message, link)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
