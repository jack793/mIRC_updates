import logging
import src.configurations as configurations

from telegram.ext import Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[
                        logging.FileHandler(configurations.LOG_FILENAME),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(configurations.API_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error_callback)

    # Start the Bot
    logging.info("Starting mIRC bot...")
    updater.start_polling()
