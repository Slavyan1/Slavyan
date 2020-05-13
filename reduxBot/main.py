# encoding: UTF-8
import telebot
import configparser
import os

from mainstruct import archive_mode, get_wooden_stat

config = configparser.ConfigParser()
config.read('settings.ini')

token = config.get('Settings', 'api')
bot = telebot.TeleBot(token)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Курс валют', 'Фото в архив')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Назад', 'Получить архив')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Ну что, начнем!', reply_markup=keyboard1)


@bot.message_handler(func=lambda m: m.text == 'Курс валют')
def beth_oven(message):
    bot.send_message(message.chat.id, get_wooden_stat())


@bot.message_handler(func=lambda m: m.text == 'Фото в архив')
def photo_in(message):
    archive_mode.activate(message.chat.id)
    bot.send_message(message.chat.id, 'Можешь добавлять фото:', reply_markup=keyboard2)


@bot.message_handler(func=lambda m: m.text == 'Назад')
def come_back(message):
    archive_mode.deactivate(message.chat.id)
    bot.send_message(message.chat.id, 'Отменено', reply_markup=keyboard1)


@bot.message_handler(func=lambda m: m.text == 'Получить архив')
def get_archive(message):
    archive_mode.get_archive(message.chat.id)
    file = open('./archive/{}.zip'.format(message.chat.id), 'rb')
    bot.send_document(message.chat.id, file, reply_markup=keyboard1)
    os.system('rm -rf ./archive/{}.zip'.format(message.chat.id))


@bot.message_handler(content_types=["photo"])
def for_mom(message):
    if archive_mode.action_mode:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filepath = './tgphoto/{}/'.format(message.chat.id)

        src = filepath + message.photo[-1].file_id

        with open(src + '.jpeg', 'wb') as new_file:
            new_file.write(downloaded_file)


bot.polling(none_stop=False, interval=0, timeout=3.5)
