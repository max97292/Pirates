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

kb_welcome = types.ReplyKeyboardMarkup(True, False)

kb_welcome.row('Назад')


def colony_antiques(message):
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_edge_market', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в магазин антиквариата', reply_markup=kb_welcome)
