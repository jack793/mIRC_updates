# -*- coding: UTF8 -*-
import os
import requests
from bs4 import BeautifulSoup


########################### PARSER CONFIGURATION ########################

# URL = "http://spacejam.ovh/New_pwd=fibra.php"  # target URL
#
# r = requests.get(URL)
# data = r.text
# soup = BeautifulSoup(data, "html.parser")


# def extract_film(cont: int, row: int, film: list) -> list:
#     if row == 10:  # Base case: I have top ten Bluray 1080p film
#         print("parsing terminated..returning the list (" + str(len(film)) + " elements inside)")
#         return film
#     else:
#         for item in soup.find_all("a", class_="titolo ricerca pos" + str(row)):
#             cont = cont + 1
#             if cont == 4:
#                 film.append(item.string)
#                 extract_film(0, row + 1, film)  # Recursion: reset counter and increase row


########################### TELEGRAM CONFIGURATION ########################


# Telegram bot API token
API_TOKEN = "TOKEN HERE"

# Path where wil be stored the configurations
SCHEDULER_CONFIG_PATH = os.path.dirname(__file__)

# File that holds the log
LOG_FILENAME = os.path.dirname(__file__) + "/result.log"


# Database file where will be stored all the events
# SQLITE_DB = os.path.dirname(__file__) + "/result.txt"

########################### BOT CONFIGURATION ########################

class BotHandler:
    def __init__(self, api_token):
        self.soup = BeautifulSoup
        self.dump = []
        self.film = []
        self.token = api_token
        self.api_url = "https://api.telegram.org/bot{}/".format(api_token)

    # URL = "https://api.telegram.org/bot<token>/"

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
    def printable(as_list: list):
        if len(as_list) == 0:
            return 'Ahia ahia la lista è vuota, c\'è qualcosa che non va'
        else:
            reversedList = as_list[::-1]  # reverse the list for increase user readability
            strDump = '\n\n- '.join(reversedList)  # Convert obj list in a string list
            return '- ' + strDump

    def get_film(self, row: int, cont: int):
        if len(self.film) == 0:
            r = requests.get(URL)   # UPDATE request data
            data = r.text
            print(' --> request to url target done')
            self.soup = BeautifulSoup(data, "html.parser")
            print(' --> mirc_bot.soup filled')
        if row == 10:  # Base case: I have top ten Bluray 1080p film
            print("parsing terminated..returning the list (" + str(len(self.film)) + " elements inside)")
            self.dump = self.film.copy()    # Crate a dump for /lista bot command
            # reversedList = self.film[::-1]  # reverse the list for increase user readability
            # strDump = '\n\n- '.join(reversedList)  # Convert list to string
            # return '- ' + strDump
            print(self.film)
            return 0
        for item in self.soup.find_all("a", class_="titolo ricerca pos" + str(row)):
            cont = cont + 1
            if cont == 4:
                self.film.append(item.string)
                self.get_film(row + 1, 0)  # Recursion: reset counter and increase row

    # def get_topten(self) -> str:
    #     """
    #     Call the extract_film method from mirc_updates and return the updated top ten list
    #     :return: updated top ten list in string format
    #     """
    #     del self.film[:]  # RESET FILM LIST BEFORE GET NEWER ONE
    #     extract_film(0, 0, self.film)  # modify 'film_list' parameter passed
    #     self.dump = self.film.copy()
    #     reversedList = self.film[::-1]  # reverse the list for increase user readability
    #     strDump = '\n\n- '.join(reversedList)  # Convert list to string
    #     return '- ' + strDump


URL = "http://spacejam.ovh/New_pwd=fibra.php"  # target URL
FILM_LIST = []
DUMP_LIST = []
bot_token = API_TOKEN  # Token of your bot

mirc_bot = BotHandler(bot_token)  # Your bot's name


########################### MAIN ##########################

def main():
    new_offset = 0
    print('Starting mIRC_bot...')
    print('mIRCbot active')

    while True:
        all_updates = mirc_bot.get_updates(new_offset)
        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']

                #######  CHECK USER INFO #######

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

                #######  CHECK USER COMMANDS  #######

                if first_chat_text == '/BLURAY':
                    mirc_bot.send_message(first_chat_id, 'Ok ' + first_chat_name +
                                          ' estraggo la TOP TEN aggiornata, attendi qualche secondo...\n\n')

                    del mirc_bot.film[:]  # RESET FILM LIST BEFORE GET NEWER ONE
                    mirc_bot.get_film(0, 0)
                    mirc_bot.send_message(first_chat_id, mirc_bot.printable(mirc_bot.film))
                    mirc_bot.send_message(first_chat_id, 'Ecco la TOP TEN aggiornata! \n - /LISTA: Rivedi l\' ultima '
                                                         'lista ottenuta;\n - /BLURAY: Aggiorna nuovamente la TOP TEN!')
                    new_offset = first_update_id + 1
                elif first_chat_text == '/LISTA':
                    if len(mirc_bot.dump) == 0:
                        mirc_bot.send_message(first_chat_id, first_chat_name + ' devi eseguire almeno una volta il '
                                                                               'comando  /BLURAY  per avere la lista '
                                                                               'aggiornata, prova subito')
                    else:
                        mirc_bot.send_message(first_chat_id, mirc_bot.printable(mirc_bot.dump))
                        mirc_bot.send_message(first_chat_id, 'Ecco la lista degli ultimi film! \n'
                                                             '- Aggiornala con /BLURAY\n'
                                                             '- /LISTA se invece vuoi vederla ancora')
                    new_offset = first_update_id + 1
                elif first_chat_text == '/info':
                    mirc_bot.send_message(first_chat_id, 'Ciao ' + first_chat_name + ' sono mIRCbot, un piccolo bot '
                                                                                     'per scovare la lista dei titoli '
                                                                                     'più belli del momento in ottima '
                                                                                     'qualità, provenienti da un '
                                                                                     'canale (segretissimo) della  '
                                                                                     'buia rete IRC! ')
                    mirc_bot.send_message(first_chat_id, 'Provami subito, in questa '
                                                         'versione (v0.3) i miei comandi '
                                                         'sono:\n - /BLURAY: Ottieni la TOP '
                                                         'TEN attuale;\n - /LISTA: Rivedi '
                                                         'l\' ultima lista ottenuta ('
                                                         'esegui almeno una volta l\' '
                                                         'aggiornamento)')
                    new_offset = first_update_id + 1
                else:
                    mirc_bot.send_message(first_chat_id, 'Benvenuto ' + first_chat_name + ' sono mIRCbot (v0.3).\nUsa '
                                                                                          'il comando /info per '
                                                                                          'sapere tutto su di me')
                    new_offset = first_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
