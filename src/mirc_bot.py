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


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(configurations.API_TOKEN)
