# -*- coding: utf-8 -*-

import emoji

from src.colony.colony import *
from src.colony.edge.store import *
from src.start_island import *

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("DataBase.db", check_same_thread=False)
cursor = conn.cursor()

def deemojify(string):
    string = emoji.demojize(string)
    if ':' in string:
        text_s = string.index(':')
        text_f = string.rindex(':')
        text_c = string[text_s:text_f + 1]
        string = string[:text_s] + string[text_f + 1:len(string)]
        string = string.strip()
        return str(string)
    else:
        return string

@bot.message_handler(commands=['start'])
def start_message(message):
    registration(message)

@bot.message_handler(content_types=['text'])
def text_content(message):
    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        player = cursor.fetchone()
    except Exception as e:
        print(e)

    if deemojify(message.text.lower()) == 'назад':
        if player[8] == 'colony':
            look_around(message)
        if player[8] == 'colony_edge_store':
            colony_edge(message)
    if deemojify(message.text.lower()) == 'осмотреться':
        #time.sleep(3)
        look_around(message)
    if deemojify(message.text.lower()) == 'поселение':
        #time.sleep(3)
        colony_start(message)
    if deemojify(message.text.lower()) == 'окраина':
        #time.sleep(3)
        colony_edge(message)
    if deemojify(message.text.lower()) == '︎ странная лавка':
        # time.sleep(3)
        store_welcome(message)
    if deemojify(message.text.lower()) == 'центр':
        #time.sleep(3)
        colony_center(message)
    if deemojify(message.text.lower()) == 'причал':
        #time.sleep(3)
        colony_pier(message)
    if deemojify(message.text.lower()) =='вернуться в поселение':
        colony_start(message)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)