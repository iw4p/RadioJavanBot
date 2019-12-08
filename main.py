#!/usr/bin/env python

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging
import requests
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
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
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("Radio Javan", callback_data=str(ONE)),
         InlineKeyboardButton("Spotify", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Welcome to Radio Javan Downloader Bot\nPlease Choose:",
        reply_markup=reply_markup
    )
    print(reply_markup)
    
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update, context):
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # Get Bot from CallbackContext
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Radio Javan", callback_data=str(ONE)),
         InlineKeyboardButton("Spotify", callback_data=str(TWO))]
        #  InlineKeyboardButton("Go Back", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
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
    bot.send_message(chat_id=chat_id, text="Now give me a link from RadioJavan.com")
    # keyboard = [
    #     [InlineKeyboardButton("Get Music Link", callback_data=str(THREE)),
    #      InlineKeyboardButton("Get Music Lyric", callback_data=str(FOUR))]
    # ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    # bot.edit_message_text(
    #     chat_id=query.message.chat_id,
    #     message_id=query.message.message_id,
    #     text="What you wanna do?",
    #     reply_markup=reply_markup
    # )
    # bot.message.reply_text("I'm sorry Dave I'm afraid I can't do that.")

    return FIRST


def two(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Go Back", callback_data=str(FIRST))]
        #  InlineKeyboardButton("Go Back", callback_data=str(start_over))]
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
    """Show new choice of buttons"""
    link, lyric = getMP3()
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
        # InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
         InlineKeyboardButton("Go Back", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=link,
        reply_markup=reply_markup
    )

    # Transfer to conversation state `SECOND`
    return SECOND


def four(update, context):
    """Show new choice of buttons"""
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
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("1019017482:AAFFM8J82uHqnZotdRXRiP2xAZWQKlGwxhM", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
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

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # This program is dedicated to the public domain under the CC0 license.
#
# """
# First, a few callback functions are defined. Then, those functions are passed to
# the Dispatcher and registered at their respective places.
# Then, the bot is started and runs until we press Ctrl-C on the command line.
#
# Usage:
# Example of a bot-user conversation using ConversationHandler.
# Send /start to initiate the conversation.
# Press Ctrl-C on the command line or send a signal to the process to stop the
# bot.
# """
#
# import logging
#
# from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
# from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
#                           ConversationHandler)
#
# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
#
# logger = logging.getLogger(__name__)
#
# GENDER, PHOTO, LOCATION, BIO = range(4)
#
#
# def start(update, context):
#     reply_keyboard = [['Boy', 'Girl', 'Other']]
#
#     update.message.reply_text(
#         'Hi! My name is Professor Bot. I will hold a conversation with you. '
#         'Send /cancel to stop talking to me.\n\n'
#         'Are you a boy or a girl?',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
#
#     return GENDER
#
#
# def gender(update, context):
#     user = update.message.from_user
#     logger.info("Gender of %s: %s", user.first_name, update.message.text)
#     update.message.reply_text('I see! Please send me a photo of yourself, '
#                               'so I know what you look like, or send /skip if you don\'t want to.',
#                               reply_markup=ReplyKeyboardRemove())
#
#     return PHOTO
#
#
# def photo(update, context):
#     user = update.message.from_user
#     photo_file = update.message.photo[-1].get_file()
#     photo_file.download('user_photo.jpg')
#     logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
#     update.message.reply_text('Gorgeous! Now, send me your location please, '
#                               'or send /skip if you don\'t want to.')
#
#     return LOCATION
#
#
# def skip_photo(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     update.message.reply_text('I bet you look great! Now, send me your location please, '
#                               'or send /skip.')
#
#     return LOCATION
#
#
# def location(update, context):
#     user = update.message.from_user
#     user_location = update.message.location
#     logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
#                 user_location.longitude)
#     update.message.reply_text('Maybe I can visit you sometime! '
#                               'At last, tell me something about yourself.')
#
#     return BIO
#
#
# def skip_location(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a location.", user.first_name)
#     update.message.reply_text('You seem a bit paranoid! '
#                               'At last, tell me something about yourself.')
#
#     return BIO
#
#
# def bio(update, context):
#     user = update.message.from_user
#     logger.info("Bio of %s: %s", user.first_name, update.message.text)
#     update.message.reply_text('Thank you! I hope we can talk again some day.')
#
#     return ConversationHandler.END
#
#
# def cancel(update, context):
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation.", user.first_name)
#     update.message.reply_text('Bye! I hope we can talk again some day.',
#                               reply_markup=ReplyKeyboardRemove())
#
#     return ConversationHandler.END
#
#
# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)
#
#
# def main():
#     # Create the Updater and pass it your bot's token.
#     # Make sure to set use_context=True to use the new context based callbacks
#     # Post version 12 this will no longer be necessary
#     updater = Updater("1019017482:AAFFM8J82uHqnZotdRXRiP2xAZWQKlGwxhM", use_context=True)
#
#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher
#
#     # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#
#         states={
#             GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
#
#             PHOTO: [MessageHandler(Filters.photo, photo),
#                     CommandHandler('skip', skip_photo)],
#
#             LOCATION: [MessageHandler(Filters.location, location),
#                        CommandHandler('skip', skip_location)],
#
#             BIO: [MessageHandler(Filters.text, bio)]
#         },
#
#         fallbacks=[CommandHandler('cancel', cancel)]
#     )
#
#     dp.add_handler(conv_handler)
#
#     # log all errors
#     dp.add_error_handler(error)
#
#     # Start the Bot
#     updater.start_polling()
#
#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()
#
#
# if __name__ == '__main__':
#     main()
