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

kb_transition = types.ReplyKeyboardMarkup(True, False)

kb_transition.row('Персонаж')


def transition(message, timer):
    try:
        cursor.execute('update status set location=? where id_player=?', ['transition', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    # bot.send_message(message.chat.id, 'Ты отправился в локацию', reply_markup=kb_transition)
    time.sleep(timer)
