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

def buy(message):
    id = message.text.lower()
    id = str(id)[5:]

    try:
        cursor.execute('select * from equipment where id_player=?', [message.from_user.id])
        equipment = cursor.fetchone()
    except Exception as e:
        print(e)
    start_pockets = equipment[2]
    pockets = equipment[2]
    have_potion = False
    if str(id).startswith('2'):
        if id in pockets:
            bot.send_message(message.chat.id, 'Данное зелье уже лежит у тебя в карманах')
            have_potion = True

    if pockets == '0':
        pockets = ''
        pockets += id
        pockets = pockets.split(',')
        pockets.sort()
        pockets = ','.join(pockets)
    else:
        pockets += ',' + id
        pockets = pockets.split(',')
        pockets.sort()
        pockets = ','.join(pockets)

    if have_potion:
        pockets = start_pockets

    try:
        cursor.execute('update equipment set pockets=? where id_player=?', [pockets, message.from_user.id])
        conn.commit()
        if str(id).startswith('1'):
            cursor.execute('select * from items where id=?', [id])
            items = cursor.fetchone()
        if str(id).startswith('2'):
            cursor.execute('select * from potions where id=?', [id])
            items = cursor.fetchone()
    except Exception as e:
        print(e)
    if pockets != start_pockets:
        bot.send_message(message.chat.id, '%s был успешно куплен' % (items[1]))
