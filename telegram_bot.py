import os

import telebot

from parse_data import get_synonyms_word
from database import DataBase, connect_db

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)

db = DataBase(connect_db())
db.create_db()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Напиши любое слово, что-бы получить его синонимы.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    telegram_id_user = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    print(telegram_id_user, username)

    word = ' '.join(message.text.lower().capitalize().split())

    if not db.get_id_user_of_db(telegram_id_user):
        db.add_user_in_db(telegram_id_user, username, first_name, last_name)

    db.add_session_in_db(telegram_id_user, word)

    if not db.get_id_word_of_db(word):
        synonyms = get_synonyms_word(word)
        if synonyms:
            db.add_word_and_symbols_in_db(word, synonyms)
            synonyms = db.get_symbols_of_db(word)
            bot.send_message(message.chat.id, ', '.join(synonyms) + '.')

        else:
            bot.send_message(message.chat.id, 'Нет синонимов.')
    else:
        synonyms = get_synonyms_word(word)
        bot.send_message(message.chat.id, ', '.join(synonyms) + '.')


bot.polling()
