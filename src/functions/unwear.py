# -*- coding: utf-8 -*-
import random
import time

import telebot
import sqlite3

from telebot import types
from src.config import TOKEN

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("DataBase.db", check_same_thread=False)
cursor = conn.cursor()

def unwear(message):
    id = message.text.lower()
    id = str(id)[8:]

    try:
        cursor.execute('select * from equipment where id_player=?', [message.from_user.id])
        equipment = cursor.fetchone()
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        cursor.execute('select * from items where id=?', [id])
        item = cursor.fetchone()
    except Exception as e:
        print(e)

    kit = equipment[1]
    pockets = str(equipment[2]).split(',')
    if kit == '0':
        bot.send_message(message.chat.id, 'Предмет отсутсвует')
    else:
        if kit != '0':
            pockets.append(kit)
            pockets.sort()
            kit = '0'

        power = status[6]
        power -= item[2]

        pockets = ','.join(pockets)

        try:
            cursor.execute('update equipment set kit=?, pockets=? where id_player=?', [kit, pockets, message.from_user.id])
            conn.commit()
            cursor.execute('update status set power=? where id_player=?', [power, message.from_user.id])
            conn.commit()
        except Exception as e:
            print(e)

        bot.send_message(message.chat.id, 'Предмет был снят')
