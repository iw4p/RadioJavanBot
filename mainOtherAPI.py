import telebot
import time

bot = telebot.TeleBot("1019017482:AAFFM8J82uHqnZotdRXRiP2xAZWQKlGwxhM")

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if 'https://www.radiojavan.com/mp3s/mp3/' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Hello, Please Enter RadioJavan link, example: https://www.radiojavan.com/mp3s/mp3/Ali-Sorena-Gonjeshkaka')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'ALPHA = FEATURES MAY NOT WORK')

@bot.message_handler(func=lambda msg: msg.text is not None and 'https://www.radiojavan.com/mp3s/mp3/' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == 'https://www.radiojavan.com/': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://api-rj-app.com/api2/mp3?id={}".format(at_text[1:])
        bot.reply_to(message, insta_link)

while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
