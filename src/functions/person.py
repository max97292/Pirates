# -*- coding: utf-8 -*-
import random
import time

import telebot
import sqlite3

from telebot import types

from src.config import TOKEN

from src.start_island import *
from src.colony.colony import *

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("DataBase.db", check_same_thread=False)
cursor = conn.cursor()

def person_show_characteristics(message):
    try:
        cursor.execute('select * from players where id=?', [message.from_user.id])
        player = cursor.fetchone()
        cursor.execute('select name from player_class')
        classes = cursor.fetchall()
    except Exception as e:
        print(e)

    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        cursor.execute('select * from equipment where id_player=?', [message.from_user.id])
        equipment = cursor.fetchone()
    except Exception as e:
        print(e)

    if status[9] == 'start_island':
        keyboard = kb_directions
    elif status[9] == 'colony':
        keyboard = kb_colony
    elif status[9] == 'colony_edge':
        keyboard = kb_colony_edge
    elif status[9] == 'colony_center':
        keyboard = kb_colony_center
    elif status[9] == 'colony_pier':
        keyboard = kb_colony_pier
    else:
        keyboard = types.ReplyKeyboardMarkup()

    if player[2] == 1:
        player_class = classes[0][0]
    if player[2] == 2:
        player_class = classes[1][0]
    if player[2] == 3:
        player_class = classes[2][0]
    if player[2] == 4:
        player_class = classes[3][0]

    if player[4] == 1:
        player_race = '🧔🏼'
    if player[4] == 2:
        player_race = '🧔'
    if player[4] == 3:
        player_race = '🧔🏿'

    if equipment[1] != '0':
        try:
            cursor.execute('select * from items where id=?', [equipment[1]])
            item = cursor.fetchone()
            weapon = '✅ ' + item[1] + ' /unwear_' + str(item[0]) + ' ' + str(item[3]) + '%⚙'
        except Exception as e:
            print(e)
    else:
        weapon = '❌ Отсутсвует'

    if equipment[2] != '0':
        #msg = ''

        try:
            cursor.execute('select * from items')
            item = cursor.fetchall()
        except Exception as e:
            print(e)

        msg = ''
        items = str(equipment[2]).split(',')
        for items_arr in items:
            for item_arr in item:
                if str(item_arr[0]) == (items_arr):
                    msg += '▶' + item_arr[1] + ' (' + str(item_arr[2]) + '💥 / ' + str(item_arr[3]) + '%⚙)' + ' /wear_' + str(item_arr[0]) + '\n'
    else:
        msg = ''

    bot.send_message(message.chat.id, '🏴‍☠ Пират %s\n'
                                      'Класс %s\n'
                                      'Специализация %s\n'
                                      '\n'
                                      'Имя: %s\n'
                                      'Уровень: %d\n'
                                      '🕛 Опыт: (%d/%d)\n'
                                      '\n'
                                      '❤ Здоровье: %d/%d\n'
                                      '🔪 Сила атаки: %d\n'
                                      '🌀 Прыть: %d\n'
                                      '🛡 Защита: %d\n'
                                      '🥄 Голод: %d/%d\n'
                                      '\n'
                                      'Экипировка:\n'
                                      '%s'
                                      '\n\n'
                                      'Содержимое карманов ?:\n'
                                      '%s'
                                      '' % (player_race,
                                            str(player_class),
                                            player[3],
                                            status[1],
                                            status[2],
                                            status[3], status[3],
                                            status[4], status[5],
                                            status[6],
                                            status[10],
                                            status[7],
                                            status[8], status[8],weapon, msg), reply_markup=keyboard)
