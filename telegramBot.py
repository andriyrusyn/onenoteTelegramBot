from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, requests, json, config, os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


webhook_url = config.webhook_url

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def log_image_to_onenote(bot, update):
    path = update.message.photo[3].get_file().file_path
	image_webhook_url = config.image_webhook_url or os.environ.get('image_webhook_url')
    print (path)
    response = requests.post(
            image_webhook_url, data=json.dumps({"image_url": path}),
            headers={'Content-Type': 'application/json'}
        )
    if response.status_code != 200:
        raise ValueError(
            'Request to Zapier returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    elif response.status_code == 200:
        print("pushed image")
        update.message.reply_text("Saving image...")
		
def log_to_onenote(bot, update):
    message = update.message.text    
    from_user = update.message.from_user.first_name.title()
	
    if "#" in message:
        # find the hashtag that was used and extract it
        hash_index = message.find("#")
        hashtag = message[hash_index:message.find(" ", hash_index)]
        
        if hashtag != "#":
            clean_message = message.replace(hashtag, "")
            response = requests.post(
                webhook_url, data=json.dumps({"text": clean_message, "sender": from_user, "hashtag":hashtag}),
                headers={'Content-Type': 'application/json'}
            )
       
            if response.status_code != 200:
                raise ValueError(
                    'Request to Zapier returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )

            elif response.status_code == 200:
                print("pushed message from " + from_user + " with hashtag: " + hashtag + " and message body: " + clean_message)
                update.message.reply_text("Thanks " + from_user + ", I just saved: " + clean_message[:50] + "...")

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, log_to_onenote))
    dp.add_handler(MessageHandler(Filters.photo, log_image_to_onenote))

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

