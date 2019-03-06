# -*- coding: UTF8 -*-
import requests
from src.configurations import *
from src.mirc_updates import extract_film


class BotHandler:
    def __init__(self, api_token):
        self.token = api_token
        self.api_url = "https://api.telegram.org/bot{}/".format(api_token)

    # url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update

    @staticmethod
    def get_topten(film: list) -> str:
        """
        Call the extract_film method from mirc_updates and return the updated top ten list
        :param film: list to be updated
        :return: updated top ten list in string format
        """
        extract_film(0, 0, film)    # modify 'film: list' parameter passed
        reversedList = film[::-1]   # reverse the list for increase user readability
        strDump = '\n\n- '.join(reversedList)   # Convert obj list in a string list
        return '- ' + strDump


bot_token = API_TOKEN  # Token of your bot
mirc_bot = BotHandler(bot_token)  # Your bot's name


def main():
    new_offset = 0
    print('Starting mIRC_bot...')

    while True:
        all_updates = mirc_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text = 'New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"

                if first_chat_text == '/film':
                    mirc_bot.send_message(first_chat_id, 'Ok ' + first_chat_name +
                                          ' estraggo la TOP TEN aggiornata' + ', attendi qualche secondo...\n\n')
                    mirc_bot.send_message(first_chat_id, mirc_bot.get_topten([]))
                    new_offset = first_update_id + 1
                else:
                    mirc_bot.send_message(first_chat_id, 'Scrivi in chat  /film  per avere la lista aggiornata')
                    new_offset = first_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
