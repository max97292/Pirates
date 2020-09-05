# -*- coding: utf-8 -*-

import emoji

from src.colony.colony import *
from src.colony.edge.store import *
from src.forest.forest import *
from src.beach.beach import *
from src.person import *
from src.start_island import *
from src.transition import *

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


@bot.message_handler(commands=['clear'])
def clear_player(message):
    try:
        cursor.execute("DELETE FROM equipment WHERE id_player=?", [message.from_user.id])
        conn.commit()
        cursor.execute("DELETE FROM players WHERE id=?", [message.from_user.id])
        conn.commit()
        cursor.execute("DELETE FROM status WHERE id_player=?", [message.from_user.id])
        conn.commit()
        bot.send_message(message.chat.id, 'Твой профиль удален из базы', reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def text_content(message):
    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        player = cursor.fetchone()
    except Exception as e:
        print(e)

    if player[8] == 'transition':
        if deemojify(message.text.lower()) == 'персонаж':
            person_show_characteristics(message)
        else:
            bot.send_message(message.chat.id, 'Воу-воу полехче ты ж куда-то уже идёшь')
    else:
        if deemojify(message.text.lower()) == 'назад':
            if player[8] == 'beach':
                transition(message, 0)
                look_around(message)
            if player[8].startswith('forest'):
                if player[8] == 'forest':
                    transition(message, 0)
                    look_around(message)
                else:
                    forest_backward(message)
            if player[8] == 'colony':
                transition(message, 0)
                look_around(message)
            if player[8] == 'colony_edge_store':
                transition(message, 0)
                colony_edge(message)

        if deemojify(message.text.lower()) == 'осмотреться':
            transition(message, 0)
            look_around(message)
        if deemojify(message.text.lower()) == 'поселение':
            transition(message, 0)
            colony_start(message)
        if deemojify(message.text.lower()) == 'окраина':
            transition(message, 0)
            colony_edge(message)
        if deemojify(message.text.lower()) == '︎ странная лавка':
            transition(message, 0)
            store_welcome(message)
        if deemojify(message.text.lower()) == 'центр':
            transition(message, 0)
            colony_center(message)
        if deemojify(message.text.lower()) == 'причал':
            transition(message, 0)
            colony_pier(message)
        if deemojify(message.text.lower()) == 'вернуться на площадь':
            transition(message, 0)
            colony_start(message)
        if deemojify(message.text.lower()) == 'лес' or deemojify(message.text.lower()) == 'свернуть в лес':
            transition(message, 0)
            forest_start(message)
        if deemojify(message.text.lower()) == 'пляж':
            transition(message, 0)
            beach_start(message)
        if deemojify(message.text.lower()) == 'двигаться дальше':
            forest_forward(message)
        if deemojify(message.text.lower()) == 'идти прямо':
            transition(message, 0)
            beach_forward(message)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
