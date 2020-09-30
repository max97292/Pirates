# -*- coding: utf-8 -*-

import emoji

from src.colony.edge.herbal_shop import *
from src.colony.pier.lighthouse import *
from src.forest.cave import *
from src.functions.buy_functional import *
from src.colony.center.market import *
from src.colony.colony import *
from src.colony.edge.antiques import *
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


@bot.message_handler(commands=['hero'])
def hero_command(message):
    person_show_characteristics(message)


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
            if player[9] == 'colony_edge_market':
                transition(message, 1)
                colony_edge(message)
            if player[9] == 'colony_center_market':
                transition(message, 1)
                colony_center(message)
            if player[9] == 'colony_edge_wicked':
                transition(message, 1)
                colony_edge(message)
            if player[9] == 'colony_edge_herbal_shop':
                transition(message, 1)
                colony_edge(message)
            if player[9] == 'colony_edge_herbal_shop_potion':
                transition(message, 1)
                colony_edge_herbal_shop(message)
            if player[9] == 'correct_health':
                transition(message, 1)
                colony_edge_herbal_shop(message)
            if player[9] == 'colony_center_hall':
                transition(message, 1)
                colony_center(message)
            if player[9] == 'colony_center_tavern':
                transition(message, 1)
                colony_center(message)
            if player[9] == 'colony_pier_lighthouse':
                transition(message, 1)
                colony_pier(message)
            if player[9] == 'colony_pier_forge':
                transition(message, 1)
                colony_pier(message)
            if player[9] == 'colony_pier_bar':
                transition(message, 1)
                colony_pier(message)
            if player[9] == '':
                transition(message, 1)
            if player[9] == '':
                transition(message, 1)
            if player[9] == '':
                transition(message, 1)
            if player[9] == '':
                transition(message, 1)
            if player[9] == '':
                transition(message, 1)

        if deemojify(message.text.lower()) == 'осмотреться':
            transition(message, 1)
            look_around(message)
        if deemojify(message.text.lower()) == 'поселение':
            transition(message, 1)
            colony_start(message)
        if deemojify(message.text.lower()) == 'окраина':
            transition(message, 1)
            colony_edge(message)
        if deemojify(message.text.lower()) == 'магазин антиквариата':
            transition(message, 1)
            colony_antiques(message)
        if deemojify(message.text.lower()) == 'злачный переулок':
            transition(message, 1)
            colony_edge_wicked(message)
        if deemojify(message.text.lower()) == 'лавка травника':
            transition(message, 1)
            colony_edge_herbal_shop(message)
        if deemojify(message.text.lower()) == 'поправить здоровье':
            transition(message, 1)
            correct_health(message)
        if deemojify(message.text.lower()) == 'восстановить здоровье':
            heal(message)
        if deemojify(message.text.lower()) == 'полка с зельями':
            # transition(message, 1)
            colony_edge_herbal_shop_potion(message)
        if deemojify(message.text.lower()) == '/use_201':
            activated_coal(message)
        if deemojify(message.text.lower()) == '/use_202':
            recovery_potion(message)
        if deemojify(message.text.lower()) == '/use_205':
            healing_potion(message)
        if deemojify(message.text.lower()) == '/use_203':
            protection_potion(message)
        if deemojify(message.text.lower()) == 'центр':
            transition(message, 1)
            colony_center(message)
        if deemojify(message.text.lower()) == 'ратуша':
            transition(message, 1)
            colony_center_hall(message)
        if deemojify(message.text.lower()) == 'рынок':
            transition(message, 1)
            colony_center_market(message)
        if deemojify(message.text.lower()) == 'торговец':
            colony_market(message)
        if deemojify(message.text.lower()) == 'кабак':
            transition(message, 1)
            colony_center_tavern(message)
        if deemojify(message.text.lower()) == 'причал':
            transition(message, 1)
            colony_pier(message)
        if deemojify(message.text.lower()) == 'маяк':
            transition(message, 1)
            colony_pier_lighthouse(message)
        if deemojify(message.text.lower()) == 'войти и осмотреться':
            select_spec(message)
            bot.register_next_step_handler_by_chat_id(message.chat.id, select_next)
        if deemojify(message.text.lower()) == 'кузня':
            transition(message, 1)
            colony_pier_forge(message)
        if deemojify(message.text.lower()) == 'бар':
            transition(message, 1)
            colony_pier_bar(message)

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
        if deemojify(message.text.lower()) == 'пещера':
            welcom_cave(message)
        if deemojify(message.text.lower()) == 'идти вперед':
            forward_cave(message)
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
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(3)
