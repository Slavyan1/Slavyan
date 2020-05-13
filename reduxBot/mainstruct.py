import requests
import os

from zipfile import ZipFile


def get_wooden_stat():
    bit = requests.get('https://blockchain.info/ticker').json()
    som = requests.get('https://nbu.uz/exchange-rates/json').json()
    rub = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    #

    return '💸Актуальный курс💸\n\n' \
           '1 BTC = ' + str(bit['USD']['15m']) + '$' \
           '\n' + '_' * 25 + '\n\n' \
           '1 USD = ' + str(som[23]['nbu_cell_price']) + ' UZS\n'\
           '1 USD = ' + str(rub['Valute']['USD']['Value']) + ' RUB'


class archive_mode:
    action_mode = False

    @classmethod
    def activate(cls, chat_id, ):
        os.system('mkdir ./tgphoto/{}'.format(chat_id))
        cls.action_mode = True

    @classmethod
    def deactivate(cls, chat_id):
        os.system('rm -rf ./tgphoto/{}'.format(chat_id))
        cls.action_mode = False

    @classmethod
    def get_archive(cls, chat_id):
        z = ZipFile('./archive/{}.zip'.format(chat_id), 'w')
        for root, dirs, files in os.walk('./tgphoto/{}/'.format(chat_id)):
            for filename in files:
                z.write(os.path.join(root, filename))
        z.close()
        cls.deactivate(chat_id)
