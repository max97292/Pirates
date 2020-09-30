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

def wear(message):
    id = message.text.lower()
    id = str(id)[6:]

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
    power = status[6]

    if id in pockets:
        try:
            cursor.execute('select * from items')
            Item = cursor.fetchall()
        except Exception as e:
            print(e)

        for item_minus in Item:
            if str(item_minus[0]) == str(kit):
                power -= item_minus[2]

        for item_arr in pockets:
            if item_arr == id:
                pockets.remove(id)
                break

        if kit == '0':
            kit = ''
            kit += id
        else:
            pockets.append(kit)
            pockets.sort()
            kit = ''
            kit += id

        if pockets == []:
            pockets = '0'
        else:
            pockets = ','.join(pockets)

        for item_equip in item:
            if str(item_equip) == kit:
                power += item[2]

        try:
            cursor.execute('update equipment set kit=?, pockets=? where id_player=?',
                           [kit, pockets, message.from_user.id])
            conn.commit()
            cursor.execute('update status set power=? where id_player=?', [power, message.from_user.id])
            conn.commit()
        except Exception as e:
            print(e)

        bot.send_message(message.chat.id, 'Предмет был одет')
    else:
        bot.send_message(message.chat.id, 'Предмет отсутсвует')
