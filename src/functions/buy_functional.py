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

    pockets = equipment[2]
    if pockets == '0':
        pockets = ''
        pockets += id
    else:
        pockets += ',' + id

    try:
        cursor.execute('update equipment set pockets=? where id_player=?', [pockets, message.from_user.id])
        conn.commit()
        cursor.execute('select * from items where id=?', [id])
        items = cursor.fetchone()
    except Exception as e:
        print(e)

    bot.send_message(message.chat.id, '%s был успешно куплен' % (items[1]))