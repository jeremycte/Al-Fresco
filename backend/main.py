import os
import logging
from apikey import TOKEN
from weather import get_weather
from reviews import search_score
from reviews import search_reviews

PORT = int(os.environ.get('PORT', 5000))

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', '8443'))

WEATHER = range(1)
REVIEWS = range(1)

def start(update, context):
    ''' Starts the conversation by introducing itself '''
    update.message.reply_text(
        " Welcome onboard! I am Al Fresco Bot. I would be assisting you in fetching the reviews for any location you would like to visit as well as how the weather may turn out! So, sit back and relax :) "
    )

def weather(update, context):
    ''' Returns a weather report for the specified location'''
    try:
        location = update.message.text

        update.message.reply_text("loading... Weather Report... ")
        new_string = location.replace("/weather", "")

        update.message.reply_text(get_weather(new_string))
    except:
        update.message.reply_text(get_weather("Singapore"))

def score(update, context):
    ''' Performs sentiment analysis to give ratings for a desired location '''
    try:
        ''' if the input is one word long '''
        # location = str(context.kwargs[0])  

        location = update.message.text
        update.message.reply_text("loading... Overall Sentiment Score... ")

        new_string = location.replace("/score", "")

        update.message.reply_text(search_score(new_string))

    except:
        update.message.reply_text("Please ensure you have spelt the location correctly")     

def reviews(update, context):
    ''' Performs sentiment analysis to give ratings for a desired location '''
    try:
        ''' if the input is one word long '''

        location = update.message.text
        update.message.reply_text("loading... Most Used Sentiments... ")
        new_string = location.replace("/reviews", "")

        update.message.reply_text(search_reviews(new_string))

    except:
        update.message.reply_text("Please ensure you have spelt the location correctly")     
    
def error(update, context):
    ''' Log Errors caused by Updates '''
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def help(update, context):
    ''' Help Command to list all features of this bot '''
    update.message.reply_text(
    ''' I can help you with the following commands: 

    /weather 'location': generate weather forecast for given location. Eg. /weather clementi 

    /score 'location': generates an overall sentiment score for the given location. Eg. /score starvista

    /reviews 'location': generates most frequent sentiments for the given location. Eg. /reviews springleafsunset 

    /website: learn more about our bot by visiting our website

    /cancel: deactivates the bot '''
    )

def website(update, context):
    ''' links to the website '''
    bot = context.bot
    chat_id = update.message.from_user.username
    bot.send_message(chat_id=update.message.chat_id, 
    text="<a href='https://hacknroll.jeremycte.com'>AlFresco Website</a>", parse_mode=ParseMode.HTML)

def cancel(update, context):
    ''' Deactivates the Bot '''
    user = update.message.from_user
    update.message.reply_text(
        "Hope you enjoyed your time here! I hope to see you again :D "
    )

def main():
    ''' Run the bot '''

    updater = Updater(
        TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("score", score))
    dispatcher.add_handler(CommandHandler("reviews", reviews))
    dispatcher.add_handler(CommandHandler("website", website))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_error_handler(error)
    
    updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN,
                      webhook_url='https://alfresco0.herokuapp.com/' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
