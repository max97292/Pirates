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


def beach_start(message):
    kb_beach = types.ReplyKeyboardMarkup(True, False)

    kb_beach.row('🚶 Идти прямо', '🌳 Свернуть в лес')  # в зависимости от цвета кожи, разный эмодзи
    kb_beach.row('⬅ Назад')

    try:
        cursor.execute('update status set location=? where id_player=?', ['beach', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать на пляж', reply_markup=kb_beach)


def beach_forward(message):
    kb_beach = types.ReplyKeyboardMarkup(True, False)

    kb_beach.row('🚶 Идти прямо', '🌳 Свернуть в лес')  # в зависимости от цвета кожи, разный эмодзи
    kb_beach.row('⬅ Назад')

    try:
        cursor.execute('update status set location=? where id_player=?', ['beach', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Ты прошелся дальше по пляжу', reply_markup=kb_beach)
