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

def store(message):
    try:
        cursor.execute('select * from items')
        items = cursor.fetchall()
    except Exception as e:
        print(e)

    count = 0

    msg = 'Доступные к покупки товары:\n\n'

    for item in items:
        count += 1
        msg += '◽%d) %s (%d💥 / %d%%⚙) (%d-%d) /buy_%d\n' % (count, item[1], item[2], item[3], item[4], item[5], item[0])

    bot.send_message(message.chat.id, msg)