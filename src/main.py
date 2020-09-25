# -*- coding: utf-8 -*-

import emoji

from src.functions.buy_functional import *
from src.colony.center.store import *
from src.colony.colony import *
from src.colony.edge.store import *
from src.enemys.enemys import *
from src.forest.forest import *
from src.beach.beach import *
from src.functions.person import *
from src.functions.wear import *
from src.functions.unwear import *
from src.start_island import *
from src.functions.transition import *

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

@bot.message_handler(commands=['en'])
def enemy(message):
    select_enemys(message)

@bot.message_handler(commands=['clear'])
def clear_player(message):
    try:
        cursor.execute("DELETE FROM equipment WHERE id_player=?", [message.from_user.id])
        conn.commit()
        cursor.execute("DELETE FROM players WHERE id=?", [message.from_user.id])
        conn.commit()
        cursor.execute("DELETE FROM status WHERE id_player=?", [message.from_user.id])
        conn.commit()
        cursor.execute("DELETE FROM enemy_status WHERE id_player=?", [message.from_user.id])
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

    time.sleep(0.1)
    if player[9] == 'transition':
        if deemojify(message.text.lower()) == 'персонаж':
            person_show_characteristics(message)
        else:
            bot.send_message(message.chat.id, 'Воу-воу полехче ты ж куда-то уже идёшь')
    else:
        if deemojify(message.text.lower()) == 'атаковать':
            attack_enemy(message)
        if deemojify(message.text.lower()) == 'обойти стороной':
            pass_by(message)
        if deemojify(message.text.lower()) == 'персонаж':
            person_show_characteristics(message)
        if deemojify(message.text.lower()) == 'назад':
            if player[9] == 'beach':
                transition(message, 1)
                look_around(message)
            if player[9].startswith('forest'):
                if player[9] == 'forest':
                    transition(message, 1)
                    look_around(message)
                else:
                    forest_backward(message)
            if player[9] == 'colony':
                transition(message, 1)
                look_around(message)
            if player[9] == 'colony_edge_store':
                transition(message, 1)
                colony_edge(message)

        if deemojify(message.text.lower()) == 'осмотреться':
            transition(message, 1)
            look_around(message)
        if deemojify(message.text.lower()) == 'поселение':
            transition(message, 1)
            colony_start(message)
        if deemojify(message.text.lower()) == 'окраина':
            transition(message, 1)
            colony_edge(message)
        if deemojify(message.text.lower()) == '︎ странная лавка':
            transition(message, 1)
            store_welcome(message)
        if deemojify(message.text.lower()) == 'рынок':
            store(message)
        if deemojify(message.text.lower()) == 'центр':
            transition(message, 1)
            colony_center(message)
        if deemojify(message.text.lower()) == 'причал':
            transition(message, 1)
            colony_pier(message)
        if message.text.startswith('/buy_'):
            buy(message)
        if message.text.startswith('/wear_'):
            wear(message)
        if message.text.startswith('/unwear_'):
            unwear(message)
        if deemojify(message.text.lower()) == 'вернуться на площадь':
            transition(message, 1)
            colony_start(message)
        if deemojify(message.text.lower()) == 'лес' or deemojify(message.text.lower()) == 'свернуть в лес':
            transition(message, 1)
            forest_start(message)
        if deemojify(message.text.lower()) == 'пляж':
            transition(message, 1)
            beach_start(message)
        if deemojify(message.text.lower()) == 'двигаться дальше':
            forest_forward(message)
        if deemojify(message.text.lower()) == 'идти прямо':
            transition(message, 1)
            beach_forward(message)


while True:
    try:
        bot.infinity_polling(none_stop=True, timeout=20)
    except Exception as e:
        print(e)
        time.sleep(5)