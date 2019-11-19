import config
import telebot
import os
import time
import random
import utils
from SQLighter import SQLighter
from telebot import types

bot = telebot.TeleBot(config.token)



@bot.message_handler(commands=["game"])
def game(message):
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[2], row[3])
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    utils.set_user_game(message.chat.id, row[2])
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = utils.get_answer_for_user(message.chat.id)

    if not answer:
        bot.send_message(message.chat.id, 'To start game type /game')
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id, 'Correct!', reply_markup=keyboard_hider)
            utils.finish_user_game(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Try again', reply_markup=keyboard_hider)
            game(message)
            #utils.finish_user_game(message.chat.id)



if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)
