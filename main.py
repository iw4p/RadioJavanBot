#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging
import requests
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


FIRST, SECOND = range(2)

ONE, TWO, THREE, FOUR = range(4)

def getMP3():

    RJAPI = "https://api-rj-app.com/api2/mp3?id="
    userLink = "https://www.radiojavan.com/mp3s/mp3/Satin-Toonesti-Eshgham"

    finalLink = userLink.split('https://www.radiojavan.com/mp3s/mp3/')[1]

    URL = RJAPI + finalLink
    data = requests.get(URL).text
    data = json.loads(data)

    lyric = data["lyric"]
    link = data["link"]
    return link, lyric


def start(update, context):

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [InlineKeyboardButton("Radio Javan", callback_data=str(ONE)),
         InlineKeyboardButton("Spotify", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Welcome to Radio Javan Downloader Bot\nPlease Choose:",
        reply_markup=reply_markup
    )

    return FIRST


def start_over(update, context):
    """Prompt same text & keyboard as `start` does but not as new message"""

    query = update.callback_query

    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Radio Javan", callback_data=str(ONE)),
         InlineKeyboardButton("Spotify", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose:",
        reply_markup=reply_markup
    )
    return FIRST


def one(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Get Music Link", callback_data=str(THREE)),
         InlineKeyboardButton("Get Music Lyric", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="What you wanna do?",
        reply_markup=reply_markup
    )
    return FIRST


def two(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Go Back", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Spotify feature is disable now, Try later.",
        reply_markup=reply_markup
    )
    return SECOND


def three(update, context):

    link, lyric = getMP3()
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
         InlineKeyboardButton("Go Back", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=link,
        reply_markup=reply_markup
    )

    return SECOND


def four(update, context):

    link, lyric = getMP3()
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Get the MP3 Link", callback_data=str(THREE)),
         InlineKeyboardButton("Go Back", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=lyric,
        reply_markup=reply_markup
    )
    return FIRST


def end(update, context):

    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END


def error(update, context):

    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater("1019017482:AAFFM8J82uHqnZotdRXRiP2xAZWQKlGwxhM", use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                    CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$')],
            SECOND: [CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                     CallbackQueryHandler(end, pattern='^' + str(TWO) + '$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()